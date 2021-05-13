## synchronized

### 1. 用法

- 用于非静态方法
- 用于静态方法
- 用于锁对象
- 用于代码块

```java
public class useSynchronized {
    //1.修饰普通方法, 锁是当前类的某一对象，即this
    public synchronized void normalMethod(){
        
    }
    
    //2.修饰静态方法，锁是useSynchronized.class
    public synchronized static void staticMethod(){
        
    }
    
    //没有同步的方法
    public void methodWithoutSync(){
        
    }

    public void methodA(){
        synchronized (useSynchronized.class){
            //3.同步代码块,锁是类对象
        }
    }
    
    public void methodB(A a){
        synchronized (a){
            //4.同步代码块
        }
    }
```

### 2.一句话总结

轻量级锁使用CAS, 底层时lock cmpxchg指令

重量级锁用的管程monitor，底层使用c++ ObjectMonitor,  是对象私有的

### 3. 锁升级

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ca8ffe97b5fa4dd6b2d4ebdcab3ddbd7~tplv-k3u1fbpfcp-watermark.image)  

其中， 无锁、偏向、轻量级锁都是在用户态；重量级锁需要向内核态申请资源

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/4354beebe0814aa88bbc0ac3f88ff6ed~tplv-k3u1fbpfcp-watermark.image)  

#### 升级过程

![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6ac575ea51e24b4ebf11876c3d312b98~tplv-k3u1fbpfcp-watermark.image)

### 4.锁升级条件

#### 偏向锁升级轻量级锁--条件：

- 只要有别的线程竞争

#### 轻量级锁升级重量级锁--条件

- 【曾经是】竞争超过10次  or  等待线程超过 1/2 CPU核数 or 耗时过长   or 有wait操作
- 【现在是】自适应的，jvm自动升级

#### 轻量级锁发生竞争时：

- 各个线程使用 CAS 操作，对对象的 markword进行比较--交换，尝试写上自己线程id

### 5.预习知识

- markWord
  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/a591ac3a12ea466aa0ed90a667d1d627~tplv-k3u1fbpfcp-watermark.image)

### 6.基本原理

- 偏向锁 
  - 在对象头markword中，写了第一个线程的thread Id，寄希望与没有人改它，所以连CAS都不用做
- 在偏向锁到轻量级锁升级的过程中，
  - 使用CAS，不停比较存储的mardWord和本线程的id
  - CAS, 底层是lock cmpxchg
- 轻量级锁(自旋锁)
  - 尝试使用CAS去 给markword写入线程独有的lockRecord起始地址 ，如果失败就一直自旋
- 重量级锁
  - 用的 monitor管程
    - synchornized 方法，JVM使用ACC_SYNCHRONIZED标识来实现。即JVM通过在方法访问标识符(flags)中加入ACC_SYNCHRONIZED来实现同步功能， 根本上也是monitorenter和monitorexit。

    - synchornized代码块，JVM使用monitorenter和monitorexit两个指令实现同步。即JVM为代码块的前后真正生成了两个字节码指令来实现同步功能的。

  - 底层使用的 c++ ObjectMonitor类来实现上面的原语，锁住的对象，在锁升级到重量级时，自动生成一个ObjectMonitor对象，作为内置锁，用来让各个线程争抢。
    - 无论上面两个指令中的哪一个，均是JVM通过调用操作系统的互斥原语mutex来实现，被阻塞的线程会被挂起、等待重新调度，会导致“用户态和内核态”两个态之间来回切换，对性能有较大影响。
      ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/55e2639ea637403b915cd8dd6e8528b0~tplv-k3u1fbpfcp-watermark.image)  

巧了，wait(), nitify(), notifyall()正是互斥量模型的原语，以及java object类的方法

> 【为什么这些方法都在Object类(而不是Thread类)呢？
>
> - 这就是该类所私有的ObjectMonitor对象的c++方法】



### 参考资料

[<<深入分析Synchronized原理>>](https://www.cnblogs.com/aspirant/p/11470858.html)