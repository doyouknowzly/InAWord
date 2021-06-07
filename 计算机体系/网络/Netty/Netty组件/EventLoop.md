# EventLoop

## 一、定义

EventLoop是一个接口，是Netty的一种抽象，表示从建立连接到处理各种事件的一个循环。

其主要依赖  **网络**和**并发** 两个JAVA 的基础包， 很清晰的说明了EventLoop的定位： **接收网络请求，并发执行任务**



在Netty的设计思路中，每个EventLoop由一个初始化后不再改变的Thread驱动，任务被提交以后，由EventLoopGroup调度资源来执行。

> 一个EventLoop可能被指派给多个Channel
>
> 但一个Channel一旦被分配给一个EventLoop， 那直到Channel被关闭前，一直是这个EventLoop提供服务，用的也是它内部的线程



## 二、组件

以NioEventLoop(最常见的EventLoop的实现类)举例，其中有以下重要的组件

- Selector

  直接就是java.nio包下的类，用来监听Socket， 

- 队列

  - ```java
    private final Queue<Runnable> taskQueue;
    ```

- 线程

  - ```java
    private volatile Thread thread;
    ```

- Channel 

  >  Netty的Channel对象 ，内部维护了NIO 的Channel对象， (靠组合，来借用人家的能力)

  将Channel注册到EventLoop的过程，其实就是将NIO的Channel注册到 EventLoop#Selector对象内

  但是，这个注册，又是通过将AbstractChannel内的一个eventLoop字段的指针，指向要 注册的EventLoop ，就是一个赋值的过程

- selectKeys

  - ```java
    private SelectedSelectionKeySet selectedKeys;
    ```

  存储所有就绪状态的Channel， EventLoop每次就遍历这个selectKeys, 拿到每一个Key之后去获取对应的Channel， 接下来再判断是就绪读or就绪写，然后再判断是放到



## 三、原理

参考文档: (https://blog.csdn.net/qq_35835624/article/details/104051336)

核心的执行流程代码如下：

```java
@Override
protected void run() {
    for (;;) {
        try {
            switch (selectStrategy.calculateStrategy(selectNowSupplier, hasTasks())) {
                case SelectStrategy.CONTINUE:// 默认实现下，不存在这个情况。
                    continue;
                case SelectStrategy.SELECT:
                    //将wakenUp字段设置为false，标识当前状态为阻塞
                    //调用select查询任务
                    select(wakenUp.getAndSet(false));
                    if (wakenUp.get()) {
                        selector.wakeup();
                    }
                default:
            }

            cancelledKeys = 0;//已取消的key的数量
            needsToSelectAgain = false;//是否需要再次选择
            final int ioRatio = this.ioRatio;//IO比率
            if (ioRatio == 100) {
                try {
                    processSelectedKeys();//处理Channel 感兴趣的就绪 IO 事件
                } finally {
                    runAllTasks();
                }
            } else {
                final long ioStartTime = System.nanoTime();
                try {
                    //运行所有普通任务和定时任务，不限制时间
                    processSelectedKeys();//Channel 感兴趣的就绪 IO 事件
                } finally {
                    final long ioTime = System.nanoTime() - ioStartTime;
                    //运行所有普通任务和定时任务，限制时间
                    runAllTasks(ioTime * (100 - ioRatio) / ioRatio);
                }
            }
        } catch (Throwable t) {
            handleLoopException(t);
        }
        try {
            if (isShuttingDown()) {
                closeAll();
                if (confirmShutdown()) {
                    return;
                }
            }
        } catch (Throwable t) {
            handleLoopException(t);
        }
    }
}
    protected void run() {
        for (;;) {
            try {
                try {
                    switch (selectStrategy.calculateStrategy(selectNowSupplier, hasTasks())) {
                    case SelectStrategy.CONTINUE:
                        continue;

                    case SelectStrategy.BUSY_WAIT:
                        // fall-through to SELECT since the busy-wait is not supported with NIO

                    case SelectStrategy.SELECT:
                        select(wakenUp.getAndSet(false));

                        // 'wakenUp.compareAndSet(false, true)' is always evaluated
                        // before calling 'selector.wakeup()' to reduce the wake-up
                        // overhead. (Selector.wakeup() is an expensive operation.)
                        //
                        // However, there is a race condition in this approach.
                        // The race condition is triggered when 'wakenUp' is set to
                        // true too early.
                        //
                        // 'wakenUp' is set to true too early if:
                        // 1) Selector is waken up between 'wakenUp.set(false)' and
                        //    'selector.select(...)'. (BAD)
                        // 2) Selector is waken up between 'selector.select(...)' and
                        //    'if (wakenUp.get()) { ... }'. (OK)
                        //
                        // In the first case, 'wakenUp' is set to true and the
                        // following 'selector.select(...)' will wake up immediately.
                        // Until 'wakenUp' is set to false again in the next round,
                        // 'wakenUp.compareAndSet(false, true)' will fail, and therefore
                        // any attempt to wake up the Selector will fail, too, causing
                        // the following 'selector.select(...)' call to block
                        // unnecessarily.
                        //
                        // To fix this problem, we wake up the selector again if wakenUp
                        // is true immediately after selector.select(...).
                        // It is inefficient in that it wakes up the selector for both
                        // the first case (BAD - wake-up required) and the second case
                        // (OK - no wake-up required).

                        if (wakenUp.get()) {
                            selector.wakeup();
                        }
                        // fall through
                    default:
                    }
                } catch (IOException e) {
                    // If we receive an IOException here its because the Selector is messed up. Let's rebuild
                    // the selector and retry. https://github.com/netty/netty/issues/8566
                    rebuildSelector0();
                    handleLoopException(e);
                    continue;
                }

                cancelledKeys = 0;
                needsToSelectAgain = false;
                final int ioRatio = this.ioRatio;
                if (ioRatio == 100) {
                    try {
                        processSelectedKeys();
                    } finally {
                        // Ensure we always run tasks.
                        runAllTasks();
                    }
                } else {
                    final long ioStartTime = System.nanoTime();
                    try {
                        processSelectedKeys();
                    } finally {
                        // Ensure we always run tasks.
                        final long ioTime = System.nanoTime() - ioStartTime;
                        runAllTasks(ioTime * (100 - ioRatio) / ioRatio);
                    }
                }
            } catch (Throwable t) {
                handleLoopException(t);
            }
            // Always handle shutdown even if the loop processing threw an exception.
            try {
                if (isShuttingDown()) {
                    closeAll();
                    if (confirmShutdown()) {
                        return;
                    }
                }
            } catch (Throwable t) {
                handleLoopException(t);
            }
        }
    }
```

大致流程总结如下: 

1. select 选择任务
2. processSelectedKeys 处理Channel 感兴趣的就绪 IO 事件
3. runAllTasks 运行所有普通任务和定时任务

<img src="https://img-blog.csdnimg.cn/20200120142521847.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1ODM1NjI0,size_16,color_FFFFFF,t_70" alt="在这里插入图片描述" style="zoom:67%;" />
