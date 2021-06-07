## AQS

是AbstractQueuedSynchronizer类的缩写，抽象队列同步器

### 1. java中的常见应用

- CountDownLatch
- ReenTrantLock
- Semphare

### 2. AQS的原理，用一句话概括

> 如果被请求的共享资源空闲，那么就将当前请求资源的线程设置为有效的工作线程，将共享资源设置为锁定状态；  
> 如果共享资源被占用，就需要一定的阻塞等待唤醒机制来保证锁分配。
>
> 这个机制主要用的是CLH队列的变体实现的，将暂时获取不到锁的线程加入到队列中等待被唤醒(防止过度自旋，浪费cpu)。  
> ![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/14ffc4f7b48e4044b1fff58c833d111c~tplv-k3u1fbpfcp-watermark.image)  


### 3. 和synchronized的区别

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/87b2133189fe4023846d0505a63f9d25~tplv-k3u1fbpfcp-watermark.image)

### 4. 为什么要有一个队列  

将获取锁失败的线程放进队列等待，仍有被唤醒并获取锁的机会，这个机会和策略由CLH队列实现；  

> CLH：Craig、Landin and Hagersten（3个外国人）队列，是单向链表，AQS中的队列是CLH变体的虚拟双向队列（FIFO），AQS是通过将每条请求共享资源的线程封装成一个节点来实现锁的分配。

### 5. CLH队列第一个节点为什么是虚节点

> 目的 ：∵节点入队不是原子操作，首节点是虚节点就是为了解决高并发场景下的线程安全问题  
> 在第一个线程设置state的时候，CLH队列为空； 在第二个线程设置的时候，CAS失败，加入CLH队列的时候，首节点Node不是线程2，而是AQS无参构造器生成的节点，第二个节点才是线程2
> ![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/227133e1eb664a66b16f9b25867e867d~tplv-k3u1fbpfcp-watermark.image)  

我们关注AQS的hasQueuedPredecessors()方法，是公平锁加锁时判断等待队列中是否存在有效节点的方法。如果返回False，说明当前线程可以争取共享资源；如果返回True，说明队列中存在有效节点，当前线程必须加入到等待队列中

```java
// java.util.concurrent.locks.ReentrantLock

public final boolean hasQueuedPredecessors() {
	// The correctness of this depends on head being initialized
	// before tail and on head.next being accurate if the current
	// thread is first in queue.
	Node t = tail; // Read fields in reverse initialization order
	Node h = head;
	Node s;
	return h != t && ((s = h.next) == null || s.thread != Thread.currentThread());
}
```

- 当h != t时： 如果(s = h.next) == null，等待队列正在有线程进行初始化，但只是进行到了Tail指向Head，没有将Head指向Tail，此时队列中有元素，需要返回True（这块具体见下边代码分析）。 
- 如果(s = h.next) != null，说明此时队列中至少有一个有效节点。
- 如果此时s.thread == Thread.currentThread()，说明等待队列的第一个有效节点中的线程与当前线程相同，那么当前线程是可以获取资源的；
- 如果s.thread != Thread.currentThread()，说明等待队列的第一个有效节点线程与当前线程不同，当前线程必须加入进等待队列
  如果之后还有线程竞争，就在队列中继续排队就行。

### 6. AQS核心方法

- 加锁 acquire()

```java
// java.util.concurrent.locks.AbstractQueuedSynchronizer

public final void acquire(int arg) {
	if (!tryAcquire(arg) && acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
		selfInterrupt();
}
```

可以看到tryAcquire是尝试拿锁，如果获取失败，才会加入队列中  
而tryAcquire(), 发现AQS内只是简单实现，实际使用时需要自己Override, 比如ReenTrantLock就自己重写了

```java
// java.util.concurrent.locks.AbstractQueuedSynchronizer

protected boolean tryAcquire(int arg) {
	throw new UnsupportedOperationException();
}
```

- 进入队列

```java
// java.util.concurrent.locks.AbstractQueuedSynchronizer

final boolean acquireQueued(final Node node, int arg) {
	boolean failed = true;
	try {
		// 标记等待过程中是否中断过
		boolean interrupted = false;
		for (;;) {
			// 获取当前节点的前驱节点
			final Node p = node.predecessor();
			// 如果p是头结点，说明当前节点在真实数据队列的首部，就尝试获取锁（别忘了头结点是虚节点）
			if (p == head && tryAcquire(arg)) {
				setHead(node);
				p.next = null; // help GC
				failed = false;
				return interrupted;
			}
			
			if (shouldParkAfterFailedAcquire(p, node) && parkAndCheckInterrupt())
				interrupted = true;
		}
	} finally {
		if (failed)
			cancelAcquire(node);
	}
}
```

可以看到，final修饰，不能被覆写。上述代码主要的思路是： 

- 开始自旋，不断尝试获取锁
- 如果获取到锁就结束，返回 ; 否则就休息一会再尝试获取锁
- finally代码块中，在获取锁最终失败后，会将节点状态置为CANCELLED
- 不断校验当前节点的前驱节点，如果状态是CANCELLED, 就剔除这个节点，将当前节点往前移动
- 如果前驱节点状态是SIGNAL(人家前驱节点有资格获取锁)，当前节点就休息(park, 阻塞)会吧
  - 借用LockSupport的静态方法park()
    - 返回当前线程的应该中断与否，上层方法会执行Thread.interrupted()进行中断
      `ps` 
- 中断和阻塞的区别
  - Java中断机制是一种协作机制，也就是说通过中断并不能直接终止另一个线程，而需要被中断的线程自己处理中断。这好比是家里的父母叮嘱在外的子女要注意身体，但子女是否注意身体，怎么注意身体则完全取决于自己
  - 中断是调用Thread.interrupt()，设置一个状态而已，true表示已中断，false表示未中断。设置线程中断不影响线程的继续执行，但是线程设置中断后，线程内调用了wait、jion、sleep方法中的一种， 立马抛出一个 InterruptedException，且中断标志被清除，重新设置为false。
  - 阻塞才能使线程真正地停下来，需要设置线程为阻塞，使用LockSupport.park(),具体原理此处不表。

### 7. 【总结】关键节点

CLH队列中Node节点的状态  
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/66f2951613ab4f8d8c99e088b1ca3507~tplv-k3u1fbpfcp-watermark.image)

- 何时入队列

  - 一个线程获取锁失败了，就会被放入等待队列。
  - acquireQueued会把放入队列中的线程不断去获取锁，直到获取成功或者不再需要获取（中断）。

- 何时出队列

  - 前置节点是头结点，且当前线程获取锁成功

- 如何出队列

- 何时阻塞

- 何时中断

- 何时唤醒
  
- 如何获取锁

- 如何释放锁

- 如何统计哪些线程在争抢锁

- 如何判断当前获得锁的是哪个线程

- 获取锁失败的线程状态

  waiting

# 参考资料
1. [美团技术博客-<<从ReentrantLock的实现看AQS的原理及应用>>](https://tech.meituan.com/2019/12/05/aqs-theory-and-apply.html)
2. [开源博客-<<Java多线程（十）之ReentrantReadWriteLock深入分析>>](http://blog.csdn.net/vernonzheng/article/details/8297230)