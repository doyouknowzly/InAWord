## Netty基础

Netty是最流行的 NIO 框架，由 JBOSS 提供的，整合了FTP,SMTP,HTTP等协议

| 序号 | 问题                                   | 一句话简介                                                   |
| ---- | -------------------------------------- | ------------------------------------------------------------ |
| 1    | Netty的优点？ 缺点？                   |                                                              |
| 2    | Netty的使用场景                        | 常用的互联网项目比如Dubbo,  ElasticSearch,  RocketMq都使用了Netty <br>大部分网络场景的业务都可以使用Netty，比如即时通讯系统IM or 消息推送系统 |
| 3    | Netty 为什么性能强                     |                                                              |
| 4    | Netty 核心组件有哪些？分别有什么作用？ |                                                              |
| 5    | Netty使用了哪些设计模式？              |                                                              |



### 1. Netty的优点？ 缺点？

优点: 

- 高效

- 支持多种协议(如 FTP，SMTP，HTTP)
- 统一的 API，支持多种传输类型，阻塞和非阻塞的
- 简单而强大的线程模型
- 比java 原生NIO性能更好
- 社区活跃
- 成熟稳定，使用的项目多

缺点: 





### 4. Netty 核心组件有哪些？分别有什么作用？

| 序号 | 组件            | 作用              | 备注                                                         |
| ---- | --------------- | ----------------- | ------------------------------------------------------------ |
| 0    | EventLoop       |                   | 每个NioEventLoop中包含了一个NIO Selector、一个队列、一个线程 |
| 1    | EventLoopGroup  | 包含多个EventLoop | 默认的构造函数实际会起的线程数为 **`CPU核心数*2`**           |
| 2    | Channel         |                   |                                                              |
| 3    | ChannelFuture   |                   |                                                              |
| 4    | ChannelHandler  |                   |                                                              |
| 5    | ChannelPipeline |                   |                                                              |
| 6    | Bootstrap       | 客户端启动辅助类  |                                                              |
| 7    | ServerBootstrap | 服务端启动辅助类  |                                                              |
|      |                 |                   |                                                              |
| 0    | NIO Selector    |                   |                                                              |







