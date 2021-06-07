# CountDownLatch

参考资料

1.[CountDownLatch的两种常用场景](https://zhuanlan.zhihu.com/p/148231820)  



## 零、用法

调用await()方法的线程会被阻塞, 直到计数器变成0才会继续执行

每次countDown()则都是release(1)减



## 一、概览





一起看看源码的注释

```java
/**
* A synchronization aid that allows one or more threads to wait until
* a set of operations being performed in other threads completes.
*
* @since 1.5
* @author Doug Lea
*/
public class CountDownLatch {
}
```

翻译如下：它是一个同步工具类，允许一个或多个线程一直等待，直到其他线程运行完成后再执行。  
通过描述，可以清晰的看出，CountDownLatch的两种使用场景：

- 场景1：让多个线程等待  

- 场景2：和让单个线程等待。

  

## 二、使用场景

### 场景1：让多个线程等待：模拟并发，让并发线程一起执行

```java
package com.zly.concurrent;

import java.util.concurrent.CountDownLatch;

public class useCountDownLatch {
    public static void main(String[] args) throws Exception{
        useCountDownLatch useCountDownLatch = new useCountDownLatch();
        useCountDownLatch.multiThreadWait();
    }

    public void multiThreadWait() throws Exception{
        CountDownLatch countDownLatch = new CountDownLatch(1);

        int i = 0;
        do{
            new Thread(() -> {
                try {
                    //运动员都阻塞在这，等待发令
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("currentThread start run");
            }).start();
            i ++;
        }while (i < 5);

        System.out.println("before run");
        Thread.sleep(2000);// 裁判准备发令
        countDownLatch.countDown();// 发令枪：执行发令
    }
}
```
 运行结果：	        
```
before run
currentThread start run
currentThread start run
currentThread start run
currentThread start run
currentThread start run
```

### 场景2:让单个线程(比如主线程)等待：多个线程(任务)完成后，进行汇总合并

```java
public void singleThreadWait() throws Exception{
    CountDownLatch countDownLatch = new CountDownLatch(5);
    for (int i = 1; i <= 5; i++) {
        final int index = i;
        new Thread(() -> {
            try {
                Thread.sleep(1000 + ThreadLocalRandom.current().nextInt(1000));
                System.out.println("finish:" + index + Thread.currentThread().getName());
                countDownLatch.countDown();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }

    countDownLatch.await();// 主线程在阻塞，当计数器==0，就唤醒主线程往下执行。
    System.out.println("主线程:在所有任务运行完成后，进行结果汇总");
}

```
运行结果：
```
finish:1Thread-5
finish:5Thread-9
finish:4Thread-8
finish:3Thread-7
finish:2Thread-6
主线程:在所有任务运行完成后，进行结果汇总
```


比如springBoot项目启动时，在spring线程处理完前，不希望主线程停止
```java
@SpringBootApplication
public class Main {
	private static final Logger logger = LoggerFactory.getLogger(Main.class);

	private static CountDownLatch closeLatch = new CountDownLatch(1);

	public static void main(String[] args) throws InterruptedException {
        new SpringApplicationBuilder()
        .sources(Main.class)
        .web(false)
        .run(args);
        logger.info("admin service start ok.");
        closeLatch.await();
	}
}
```



## 三、原理



1、思路

- CountDownLatch是通过一个计数器来实现的，计数器的初始值为线程的数量；  
- 调用await()方法的线程会被阻塞，直到计数器 减到 0 的时候，才能继续往下执行；
- 调用了await()进行阻塞等待的线程，它们阻塞在Latch门闩/栅栏上；只有当条件满足的时候（countDown() N次，将计数减为0），它们才能同时通过这个栅栏；以此能够实现，让所有的线程站在一个起跑线上。 

2、原理细节

- 底层基于 AbstractQueuedSynchronizer 实现，CountDownLatch 构造函数中指定的count直接赋给AQS的state；

- 每次countDown()则都是release(1)减1，最后减到0时unpark阻塞线程；这一步是由最后一个执行countdown方法的线程执行的。

- 而调用await()方法时，当前线程就会判断state属性是否为0，如果为0，则继续往下执行

- 如果不为0，则使当前线程进入等待状态，直到某个线程将state属性置为0，其就会唤醒在await()方法中等待的线程。



## 四、对比

- vs CyclicBarrier
   CountDownLatch和CyclicBarrier都能够实现线程之间的等待，只不过它们侧重点不同：
  - CountDownLatch一般用于一个或多个线程，等待其他线程执行完任务后，再才执行
  - CyclicBarrier一般用于一组线程互相等待至某个状态，然后这一组线程再同时执行
  - 另外，CountDownLatch是减计数，计数减为0后不能重用；而CyclicBarrier是加计数，可置0后复用。

- vs Thread.join()
  - CountDownLatch的作用就是允许一个或多个线程等待其他线程完成操作，看起来有点类似join() 方法，但其提供了比 join() 更加灵活的API
  - CountDownLatch可以手动控制在n个线程里调用n次countDown()方法使计数器进行减一操作，也可以在一个线程里调用n次执行减一操作。
  - 而 join() 的实现原理是不停检查join线程是否存活，如果 join 线程存活则让当前线程永远等待。所以两者之间相对来说还是CountDownLatch使用起来较为灵活

