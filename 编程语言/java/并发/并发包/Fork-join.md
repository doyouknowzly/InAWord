# Fork-join

![img](https://pic1.zhimg.com/80/v2-27087afc113c5a5c0cc5f2e95c1eb3c8_720w.jpg)



参考文章: https://zhuanlan.zhihu.com/p/68554017



fork-join 首先是一种并行模型，以 fork (开启)分支的方式执行代码逻辑，待全部分支递归执行完毕，join (合并)所有并行分支，而后代码会继续串行执行。

从算法角度上来说，特别适合**基于分治法**的计算



## 一、传统线程池模型

![img](https://pic3.zhimg.com/80/v2-802762b600b6cae171fae57a1ed37042_720w.jpg)

传统的线程池的实现大致是这样的：

- 首先生成一个线程池需要指定核心线程数（coreSize）、最大线程数（maxSize）、work queue 阻塞队列初始化、线程创建工厂类（ThreadFactory）以及阻塞队列满员后的丢弃策略等等。

- 任务不会马上 offer 到 work queue，而是逐步创建好足够数量（coreSize）的线程作为核心线程（worker thread），只要 worker thread 的数量小于 coreSize ，就继续创建下去，因此最早这批 task 会先和 worker thread 绑定，绑定完成后 worker thread也随之启动（Thread.start()）。



worker thread 和 task 是 1:N 的关系，task 并非是真正的线程实例，相对 1:1 而言，这种方式更加轻量；线程池相对于普通线程创建而言，线程数量是可控的；核心线程在执行过程中不会被回收，可以对核心线程资源充分利用，减少了线程上下文切换的成本。



缺点： 



## 二、Fork-join模型

- worker thread 是给定的，由OS直接调度，这点和传统线程池一致。通常，worker thread 会和处理器核心数量保持一致；
- F-J task 都是轻量级执行实例，worker thread 和 task 同样是 1:N 的关系 ；
- 通过 work queue 管理任务，worker thread 执行任务。与传统线程池不同是，传统线程池只会维护一个 work queue；而 F-J pool 中的每个 worker thread 都独立维护一个 work queue。



### 2.1 工作量窃取**(work-stealing)**

![img](https://pic3.zhimg.com/80/v2-d3caf6a7ebb4919413ec845e0cf5d89e_720w.jpg)

F-J 核心就在于**轻量级**的调度（相对于传统线程池而言)，理解了 work-stealing 就理解了 F-J 的调度算法。

简单来说，就是 **空闲的线程试图从繁忙线程的 deques 中 *窃取* 工作**。



为了提供有效的并行执行，fork/join 框架使用了一个名为 `ForkJoinPool` 的线程池，用于管理 `ForkJoinWorkerThread` 类型的工作线程

- `ForkJoinPool` 线程池并不会为每个子任务创建一个单独的线程，相反，池中的每个线程都有自己的双端队列用于存储任务 （ double-ended queue ）( 或 deque，发音 `deck` ）。

- 默认情况下，每个工作线程从其自己的双端队列中获取任务。但如果自己的双端队列中的任务已经执行完毕，双端队列为空时，工作线程就会从另一个忙线程的双端队列尾部或全局入口队列中获取任务，因为这是最大概率可能找到工作的地方。

