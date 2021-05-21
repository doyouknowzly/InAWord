| 序号 | 问题                          | 一句话描述 |
| ---- | ----------------------------- | ---------- |
| 0    | epoll的思路                   |            |
| 1    | epoll的结构体、各个组件的作用 |            |
| 2    | epoll原理详解                 |            |
| 3    | epoll的ET、LT模式             |            |
| 4    | epoll惊群问题                 |            |
|      |                               |            |

参考Linux官方文档 (https://man7.org/linux/man-pages/man7/epoll.7.html)



### 1. epoll的结构体、各个组件的作用

```cpp
//用户数据载体
typedef union epoll_data {
   void    *ptr;
   int      fd;
   uint32_t u32;
   uint64_t u64;
} epoll_data_t;
//fd装载入内核的载体
 struct epoll_event {
     uint32_t     events;    /* Epoll events */
     epoll_data_t data;      /* User data variable */
 };
 //三板斧api
int epoll_create(int size); 
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);  
int epoll_wait(int epfd, struct epoll_event *events,
                 int maxevents, int timeout);
```

| 组件 | 作用 |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |
|      |      |      |
|      |      |      |



### 2. epoll原理详解

参考文档 (https://zhuanlan.zhihu.com/p/87843750)

select低效的原因之一是将“维护等待队列”和“阻塞进程”两个步骤合二为一。每次调用select都需要这两步操作，然而**大多数应用场景中，需要监视的socket相对固定，并不需要每次都修改**



所以epoll()采用了三步， 分别是**epoll_create()、epoll_ctl()、epoll_wait()** ，先用epoll_ctl**维护等待队列**，再调用epoll_wait**阻塞进程**。显而易见的，效率就能得到提升

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200322191643279.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bnhpYW5naHVhbmc=,size_16,color_FFFFFF,t_70)



- epoll_create()  

  用户进程通过 **epoll_create() **函数在内核空间里面创建了一块空间（为了便于理解，可以想象成创建了一块白板），并返回了描述此空间的fd。

- epoll_ctl()

  通过**epoll_ctl() **我们可以通过自定义的epoll_event结构体在这块"白板上"注册感兴趣的事件了。

  1. 把socket放到对应的红黑树上
  2. 还会给内核中断处理程序注册一个回调函数，告诉内核，如果这个句柄的中断了，就把它放到准备就绪rdlist链表里
  3. 所以，如果一个socket上有数据到了，内核除了把网卡上的数据copy到内存中，还会把该socket插入到准备就绪链链表里。

- epoll_wait()

  1. 如果代码运行到了**epoll_wait()** ，内核会将进程A放入eventpoll的等待队列中，进程A会一直阻塞等待
  2. 当socket接收到数据，硬盘、网卡等硬件设备数据准备完成后发起**硬中断**，中断CPU。
  3. 中断程序会操作eventpoll对象，而不是直接操作进程。中断程序一方面修改rdlist，另一方面唤醒eventpoll等待队列中的进程，进程A再次进入运行状态。也因为rdlist的存在，进程A可以知道哪些socket发生了变化

