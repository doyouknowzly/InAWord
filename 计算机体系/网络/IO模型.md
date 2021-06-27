# IO模型



| 序号 | 问题                   | 一句话简介                                                   |
| ---- | ---------------------- | ------------------------------------------------------------ |
| 0    | IO模型                 | 参考文档 (https://juejin.cn/post/6844904000496599054)<br><br/>阻塞IO (BIO)<br>非阻塞IO (NIO)<br/>IO多路复用<br/>信号驱动IO<br/>异步IO(AIO)<br> |
| 1    | 同步异步 vs 阻塞非阻塞 |                                                              |
| 2    | IO模型的底层原理       |                                                              |
| 3    | java IO的历史          | jdk1.4之前是采用同步阻塞模型（BIO）<br>jdk1.4之后推出NIO,支持非阻塞 IO<br>jdk1.7 升级推出 NIO2.0，提供了AIO 功能，支持文件和网络套接字的异步 IO |
| 4    | linux AIO              |                                                              |
|      |                        |                                                              |
| 6    | Reactor模式            |                                                              |



## 0.IO模型

- 阻塞IO (BIO)

- 非阻塞IO (NIO)

  用户进程不断轮询，询问内核数据准备好了没有

  缺点: 需要让用户进程不断切换到内核态

- IO多路复用

- 信号驱动IO

- 异步IO(AIO)

前 4 种是同步 IO，在内核数据 copy 到用户空间时是阻塞的。



## 1. 同步异步 vs 阻塞非阻塞

​	**阻塞和非阻塞：**读写没有就绪或者读写没有完成，函数是否要一直等待还是采用轮询；

​	**同步和异步：**同步是读写由应用程序完成。异步是读写由操作系统来完成，并通过回调的机制通知应用程序。



## 2. IO模型的底层原理

参考文档:

(https://www.zhihu.com/question/32163005)

(https://www.jianshu.com/p/598013bd35d6)

 (https://zhuanlan.zhihu.com/p/63179839)

![img](https://pic2.zhimg.com/80/v2-14e0536d872474b0851b62572b732e39_720w.jpg)



IO模型本质是用户线程的调度策略，底层都是调用系统调用来实现的， 比如:

- select() 

  - 1983年在BSD里面实现的

    >  BSD 代表“Berkeley Software Distribution，伯克利软件套件”, 和Linux类似， 都是免费的，开源的，类Unix系统

  - 原理:  

    1. 使用位图算法bitmap

       - 有一个长度固定为1024的数组，数组中每个元素都是0 or 1，如果是1，就代表该位置映射的fd有读写事件。

       - 比如{1, 2, 3, 5, 7}，在某种hash()算法中，就就标记为"01110101"  

    2. 只有内核态能感知到socket的事件， 所以select()就是用户进程将监听的socket对应在bitmap上标记为1，然后传给内核

    3. 内核来轮询bitmap上表示的各个socket，当有读写事件时，将bitmap原封不动的返回给用户进程

  - 优点:  算法消耗内存少

  - 缺点: 

    - 线程不安全，且官方文档中明确表示了
    - select 只能监视1024个链接
    - select 仅仅会返回【有个socket有数据啦！】，但是并不会告诉你哪个socker上有数据，于是你只能自己一个一个的找，在TCP连接数较多的时候，需要遍历，复杂度O(n)
    - 会修改入参的数组， 每次操作完都要全部清0

    

- poll()

  - 1997年实现
  - 原理 ：
    - **poll()**和**select()**是非常相似的, 唯一的区别在于**poll()**摒弃掉了位图算法，使用自定义的结构体**pollfd**
    - 在**pollfd**内部封装了fd，并通过event变量注册感兴趣的可读可写事件(**POLLIN、POLLOUT**)，最后把 **pollfd**[]数组交给内核
    - 当有读写事件触发的时候，我们可以通过轮询 **pollfd**，判断event确定该fd是否发生了可读可写事件
  - 优点: 
    - 去除了1024的限制
    - 不修改入参的数组了， 修改pollfd结构体中的event即可
    - 轮询是用户进程做的， 内核只需要给pollfd[]中，有事件的对应的fd中的event修改为**POLLIN、POLLOUT**即可
  - 缺点: 
    -  仍然线程不安全
    -  仍然存在用户态-内核态切换
    -  还是要轮询O(n)

  

- epoll()

  - 2002 年实现

  - 优点:  解决了select()的所有问题

    - O(1)复杂度，返回的"nfds"，只关联了状态改变的fd，相比于之前循环n次来确认，复杂度降低了不少；

  - 缺点:  只有linux支持， BSD不支持 (BSD上面对应的实现是kqueue).

  - 应用: Nginx、Redis等都广泛地使用了此种模式

    



## 3.Linux Aio

参考文章 (https://zhuanlan.zhihu.com/p/364819119)

### Linux原生AIO实现

一般来说，使用 Linux 原生 AIO 需要 3 个步骤：

- 1) 调用 io_setup 函数创建一个一般 IO 上下文。
- 2) 调用 io_submit 函数向内核提交一个异步 IO 操作。
- 3) 调用 io_getevents 函数获取异步 IO 操作结果。

所以，我们可以通过分析这三个函数的实现来理解 Linux 原生 AIO 的实现。

> Linux 原生 AIO 实现在源码文件 /fs/aio.c 中。



## 6. Reactor**线程模型** 是什么

大家可能会经常听到2种模式：**Reactor和Preactor**

- **Reactor 模式：主动模式。**
- **Preactor 模式：被动模式。**

> Reactor 线程模型基于事件驱动，采用I/O 多路复用统一监听事件，收到事件后分发(Dispatch 给某进程)

Reactor**线程模型**核心组成部分包括Reactor和线程池，其中Reactor负责监听和分配事件，线程池负责处理事件，而根据Reactor的数量和线程池的数量，又将Reactor分为三种模型:

- 单线程模型 (单Reactor单线程)
- 多线程模型 (单Reactor多线程)
- 主从多线程模型 (多Reactor多线程)



下图是多线程模型

<img src="http://ifeve.com/wp-content/uploads/2019/08/image-4-1024x741.png" alt="img" style="zoom:50%;" />