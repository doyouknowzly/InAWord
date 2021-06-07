# CyclicBarrier

参考资料

1.[CyclicBarrier多任务协同的利器](https://zhuanlan.zhihu.com/p/148521577)



## 一、概览

源码注释如下：

```java
/* A synchronization aid that allows a set of threads to all wait foreach other to reach 
a common barrier point.  CyclicBarriers areuseful in programs involving a fixed sized 
party of threads thatmust occasionally wait for each other. The barrier is called
<em>cyclic</em> because it can be re-used after the waiting threads are released.
*/
```



示意图解:

![img](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ebab5a91df854b9ca5960e2561540890~tplv-k3u1fbpfcp-watermark.image)



环形指的是，当所有等待线程都被释放以后，CyclicBarrier可以被重用

>  CyclicBarrier 的计数器有自动重置的功能，当减到 0 的时候，会自动重置你设置的初始值，自动复原。这个功能用起来实在是太方便了。

栅栏指的是，锁住多个线程，让大家一起等待



## 二、用法

```java
CyclicBarrier(int parties, Runnable barrierAction);
```

通过构造器的参数barrierAction 可以指定一个善后处理的task，在所有人都到达屏障点时，来执行；

- CyclicBarrier 的回调函数，可以指定一个线程池来运行，相当于异步完成；
- 如果不指定线程池，默认在最后一个执行await()的线程执行，相当于同步完成。



```java

   package com.zly.concurrent;

   import java.util.concurrent.CyclicBarrier;

   public class useCyclicBarrier {
       static int state = 1;
       static int total = 5;
       public static void main(String[] args) {


         CyclicBarrier cyclicBarrier = new CyclicBarrier(total, new Runnable() {
             @Override
             public void run() {
                 System.out.println("完成第" + state + "阶段！！------");
                 state ++;
             }
         });
         for(int i = 0; i< total; i++){
             new Thread( () -> {
                 String name = Thread.currentThread().getName();
                 try {
                     //1. 上班开早会
                     System.out.println("上班开早会~" + name);

                     cyclicBarrier.await();

                     //集合准备工作

                     //2.开始工作
                     System.out.println("工作ing~" + name);
                     //集合准备吃饭
                     cyclicBarrier.await();
                     //3.吃饭
                     System.out.println("吃饭啦！！" + name);
                 }catch (Exception e){
                     e.printStackTrace();
                 }
             }).start();
         }
     }
 }

```



运行结果：

```
   上班开早会~Thread-0
   上班开早会~Thread-3
   上班开早会~Thread-2
   上班开早会~Thread-1
   上班开早会~Thread-4
   完成第1阶段！！------
   工作ing~Thread-4
   工作ing~Thread-2
   工作ing~Thread-1
   工作ing~Thread-0
   工作ing~Thread-3
   完成第2阶段！！------
   吃饭啦！！Thread-3
   吃饭啦！！Thread-4
   吃饭啦！！Thread-2
   吃饭啦！！Thread-0
   吃饭啦！！Thread-1

```



## 三、原理

基于ReentrantLock和Condition



```java
/** The lock for guarding barrier entry */
private final ReentrantLock lock = new ReentrantLock();
/** Condition to wait on until tripped */
private final Condition trip = lock.newCondition();
/** The number of parties */
private final int parties;
/* The command to run when tripped */
private final Runnable barrierCommand;
/** The current generation */
private Generation generation = new Generation();

```

核心逻辑是在dowait()里，使用ReentrantLock上锁，每await()一次， --count; 直到count==0, 触发更新换代逻辑



```java
private int dowait(boolean timed, long nanos){

    //省略
    int index = --count;
    if (index == 0) {  // tripped
        boolean ranAction = false;
        try {
            final Runnable command = barrierCommand;
            if (command != null)
                command.run();
            ranAction = true;
            nextGeneration();
            return 0;
        } finally {
            if (!ranAction)
                breakBarrier();
        }
    }
    //省略
}

```



下面是环形，更新换代的逻辑

```java
private void nextGeneration() {
    // signal completion of last generation
    trip.signalAll();
    // set up next generation
    count = parties;
    generation = new Generation();
}

```



## 四、有趣的问题

- 屏障破坏 BrokenBarrierException
  某些情况下，屏障会被破坏，等在屏障的线程都会被释放，详见[CyclicBarrier的克星—BrokenBarrierException](https://zhuanlan.zhihu.com/p/148964094)