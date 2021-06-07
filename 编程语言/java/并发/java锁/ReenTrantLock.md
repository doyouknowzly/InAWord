## ReentrantLock

### 1. 原理  

**CAS + AQS**

```java
// java.util.concurrent.locks.ReentrantLock#NonfairSync

// 非公平锁
static final class NonfairSync extends Sync {
	...
	final void lock() {
		if (compareAndSetState(0, 1))
			setExclusiveOwnerThread(Thread.currentThread());
		else
			acquire(1);
		}
  ...
}
```

### 2. 和ReenTrantReadWriteLock的区别

它和后者都分别实现了AQS，彼此之间没有继承或实现的关系。

> ReenTrantLock是互斥锁（独占锁）， 也就是一次只能有一个线程持有锁
>
> ReenTrantReadWriteLock是共享锁， 一个资源能够被多个读线程访问，或者被一个写线程访问，但是不能同时存在读写线程。  
> 也就是说读写锁使用的场合是一个共享资源被大量读取操作，而只有少量的写操作（修改数据）

### 3. 加锁和解锁流程

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/66c3518f4e7a49978a8db9214eae8b39~tplv-k3u1fbpfcp-watermark.image)

## Atomic类

### 1. 一句话总结

- atomic类是通过自旋+CAS操作+volatile变量实现的。
  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d0e962ca948d4c2285f77bd0e16203a8~tplv-k3u1fbpfcp-watermark.image)

### 2. jdk8 的LongAdder 和 AtomicLong相比，优化了哪里？

高并发下N多线程同时去操作一个变量会造成大量线程CAS失败，然后处于自旋状态，导致严重浪费CPU资源，降低了并发性。既然AtomicLong性能问题是由于过多线程同时去竞争同一个变量的更新而降低的，那么如果把一个变量分解为多个变量，让同样多的线程去竞争多个资源，这就是LongAdder的原理。  
![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5074a82ac3014db2a0233a383ad6f8ca~tplv-k3u1fbpfcp-watermark.image)  
LongAdder则是内部维护一个Cells数组，每个Cell里面有一个初始值为0的long型变量，在同等并发量的情况下，争夺单个变量的线程会减少，这是变相的减少了争夺共享资源的并发量，另外多个线程在争夺同一个原子变量时候，如果失败并不是自旋CAS重试，而是尝试获取其他原子变量的锁，最后当获取当前值时候是把所有变量的值累加后再加上base的值返回的。



# 参考资料
1. [美团技术博客-<<从ReentrantLock的实现看AQS的原理及应用>>](https://tech.meituan.com/2019/12/05/aqs-theory-and-apply.html)
2. [开源博客-<<Java多线程（十）之ReentrantReadWriteLock深入分析>>](http://blog.csdn.net/vernonzheng/article/details/8297230)