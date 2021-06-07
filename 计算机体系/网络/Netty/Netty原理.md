## Netty原理

| 序号 | 问题                             | 一句话简介                                                   |
| ---- | -------------------------------- | ------------------------------------------------------------ |
| 0    | Netty和Nio的关系                 | java有NIO包去实现非阻塞的网络IO，但NIO包太复杂了，写代码很冗长<br>所以Netty做了封装,使用 Netty可以高效开发，但底层还是使用java NIO的代码 |
| 1    | IO多路复用是什么？ Netty怎么用的 |                                                              |
| 2    | Netty 线程模型                   |                                                              |
| 3    | Netty 长连接、心跳机制           |                                                              |
| 4    | Netty 解决TCP粘包、拆包问题      |                                                              |
| 5    | TCP 半包读写问题                 |                                                              |

### 1. IO多路复用是什么？ Netty怎么用的

IO多路复用，英文全称是 **I/O multiplexing**

I/O 是指网络 I /O ，多路指多个 TCP 连接，复用指一个或几个线程。

- 思路:   
  - 使用一个或者几个线程处理多个 TCP 连接，不必创建过多的线程进程，也不必维护这些线程进程。
  - 哪个TCP连接有数据了，当前线程就开始读写这个TCP
  - 底层一般使用epoll()来实现 
    - 当然，select(), poll()也可以， 只是效率没有epoll高
  
- 目的： 尽量多的提高服务器的吞吐能力 (因为需要创建的线程少了，减少了CPU和内存的浪费)





<img src="https://pic4.zhimg.com/80/18d8525aceddb840ea4c131002716221_720w.jpg?source=1940ef5c" alt="img" style="zoom: 67%;" />

在同一个线程里面， 通过拨开关的方式，来同时传输多个I/O流， (学过EE的人现在可以站出来义正严辞说这个叫 “时分复用” 了）。

> JDK为了保证多平台通用，所以某些情况下JDK NIO的API性能不及Netty专门用C语言写的API，举例:
>
> 如果确定只在linux平台上使用，其实可以使用EpollEventLoopGroup，会有较少的gc，性能更好

那该如何使用native socket transport（epoll）呢？

其实只需将相应的类替换即可

| 默认使用NIO API的      | Netty自己实现的               |
| ---------------------- | ----------------------------- |
| NioEventLoopGroup      | EpollEventLoopGroup<br/>      |
| NioEventLoop           | EpollEventLoop<br/>           |
| NioServerSocketChannel | EpollServerSocketChannel<br/> |
| NioSocketChannel       | EpollSocketChannel            |



### 2. Netty 线程模型

1.  线程分配

   ### 注意截止2021.5.22 Dubbbo 2.7版本还是使用Netty3， 只保证入站事件会在IO线程里执行
   
   Netty4版本已经取消了这个复杂的设计， 即一个连接的所有事件都由一个线程来处理完，即EventLoop里面的那个Thread, 
   
   目的: 简化设计，避免复杂的线程同步，  避免一些情况下的上下文切换的开销
   
2. 任务执行

   - 检查任务的调用线程是否是分配给EventLoop的那个线程
     - 如果是， 就直接立即执行
     - 如果不是，进入EventLoop的内部队列里等一会，等到下次这个Channel有新的事件时再处理
