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



# 参考资料
1. [美团技术博客-<<从ReentrantLock的实现看AQS的原理及应用>>](https://tech.meituan.com/2019/12/05/aqs-theory-and-apply.html)
2. [开源博客-<<Java多线程（十）之ReentrantReadWriteLock深入分析>>](http://blog.csdn.net/vernonzheng/article/details/8297230)