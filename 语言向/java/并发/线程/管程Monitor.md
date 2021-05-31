# 管程Monitor



## 一、作用

操作系统中，semaphore 信号量 和 mutex 互斥量是最重要的同步原语

**管程是一种抽象，为了防止底层mutex互斥量太难写、容易写错的问题，抽象出的一层高级原语**

在Java中是ObjectMonitor（1个C++类）， 来实现monitor管程这个概念

> 需要注意的是，操作系统本身并不支持 monitor 机制，实际上，monitor 是属于编程语言的范畴



## 二、定义

#### **monitor基本元素：**

1. **临界区**     

   被 synchronized 关键字修饰的方法、代码块，就是 monitor 机制的临界区。

2. **monitor 对象** (锁) 

3. **条件变量**

![clipboard.png](https://segmentfault.com/img/bVbtXwv?w=404&h=542)



1、同一个时刻，只有一个 进程/线程 能进入 monitor 中定义的临界区，这使得 monitor 能够达到互斥的效果。

2、但仅仅有互斥的作用是不够的，无法进入 monitor 临界区的 进程/线程，它们应该被阻塞，并且在必要的时候会被唤醒



## 三、java Monitor数据结构

在线程竞争激烈的时候，锁会升级为重量级锁，指的就是锁的对象的MardWord (参考[<<MardWord>>](./MarkWord))中，monitor指针指向的ObjectMonitor对象





**monitor（lockRecord）详情:**

monitor是线程私有的数据结构，每一个线程都有一个可用monitor列表，同时还有一个全局的可用列表，先来看monitor的内部

![image.png](https://cdn.nlark.com/yuque/0/2020/png/1164655/1594734144851-23b1185c-4549-4ce6-bbb7-70a3543ea392.png)

## 四、原理

java.lang.Object 类定义了 wait()，notify()，notifyAll() 方法，这些方法的具体实现，依赖于一个叫 ObjectMonitor 模式的实现，基本原理如下

![img](G:\有道云\data\zlyforwork@126.com\40dc9c3291cb4838b6b151851e4ce608\clipboard.png)

- **图将 Monitor 相关线程分为 3 类：**
  - **entry set**：**从未** 获取过 Monitor 的线程，排队竞争 Monitor；
  - **owner**：同一时刻，只有一个线程持有 Monitor；
  - **wait set**：**曾经持有** Monitor 的线程，通过 `Object.wait()` 主动进入 wait set；
  
  > 两种set 底层都是C++代码实现的链表



- **首次进入**

  - 要获取 Monitor，通道只有一条，即 entry set，若线程 t 进入 entry set 后发现：

    - Monitor 当前未被持有；
    - entry set 只有自己一个线程在等待；

  - 则 t 可立即获取 Monitor。



- **释放 Monitor**

  - 若 Monitor 当前被线程 t 持有，根据 t 释放 Monitor 前是否执行 `notify`
  - 执行过 `notify`，则 entry set 和 wait set 中的线程一起竞争 Monitor；
  - 未执行 `notify`，则只有 entry set 中的线程一起竞争 Monitor；



- **超时版** **`wait(t)`**

  若线程 t 使用带超时参数的 `wait(t)`，则超过 t 时间后，即使没有线程执行 `notify`，t 也会自动从 wait set 中被取出，从而竞争 Monitor，

  这里超时相当于隐式的被 `notify`。




>  **notify vs notifyAll**
>
> - `notify` 只会从 wait set **随机** 选取一个线程唤醒；
>
> - 而 `notifyAll` 会唤醒 wait set 中的所有线程，不过最多只有一个能成功获取 Monitor，其余会再次进入 wait set。



