### Dubbo网络层



网络层主要包含下图的Protocol, Exchange, Transport, Serialize 4层

![image-20210521103813815](D:\Users\80233448\AppData\Roaming\Typora\typora-user-images\image-20210521103813815.png)

| 序号 | 问题            | 一句话描述 |
| ---- | --------------- | ---------- |
| 0    | Dubbo缺省协议   |            |
| 1    | Dubbo的线程模型 |            |
| 2    | Dubbo线程池策略 |            |
|      |                 |            |
|      |                 |            |
|      |                 |            |
|      |                 |            |
|      |                 |            |
|      |                 |            |



### 0. Dubbo缺省协议

参考官方文档 (https://dubbo.apache.org/zh/docs/v2.7/user/examples/thread-model/)

（https://dubbo.apache.org/zh/docs/v2.7/user/references/protocol/dubbo/）

Dubbo 缺省协议采用单一长连接和 NIO 异步通讯，适合于小数据量大并发的服务调用，以及服务消费者机器数远大于服务提供者机器数的情况。

反之，Dubbo 缺省协议不适合传送大数据量的服务，比如传文件，传视频等，除非请求量很低。

![dubbo-protocol.jpg](https://dubbo.apache.org/imgs/user/dubbo-protocol.jpg)

- Transporter: mina, netty, grizzy
- Serialization: dubbo, hessian2, java, json
- Dispatcher: all, direct, message, execution, connection
- ThreadPool: fixed, cached

### 特性

缺省协议，使用基于 netty `3.2.5.Final` 和 hessian2 `3.2.1-fixed-2(Alibaba embed version)` 的 tbremoting 交互。

- 连接个数：单连接
- 连接方式：长连接
- 传输协议：TCP
- 传输方式：NIO 异步传输
- 序列化：Hessian 二进制序列化
- 适用范围：传入传出参数数据包较小（建议小于100K），消费者比提供者个数多，单一消费者无法压满提供者，尽量不要用 dubbo 协议传输大文件或超大字符串。
- 适用场景：常规远程服务方法调用

### 约束

- 参数及返回值需实现 `Serializable` 接口
- 参数及返回值不能自定义实现 `List`, `Map`, `Number`, `Date`, `Calendar` 等接口，只能用 JDK 自带的实现，因为 hessian 会做特殊处理，自定义实现类中的属性值都会丢失。
- Hessian 序列化，只传成员属性值和值的类型，不传方法或静态变量，兼容情况 [1](https://dubbo.apache.org/zh/docs/v2.7/user/references/protocol/dubbo/#fn:1)[2](https://dubbo.apache.org/zh/docs/v2.7/user/references/protocol/dubbo/#fn:2)：



### 常见QA:

#### 为什么要消费者比提供者个数多?

因 dubbo 协议采用单一长连接，假设网络为千兆网卡 [3](https://dubbo.apache.org/zh/docs/v2.7/user/references/protocol/dubbo/#fn:3)，根据测试经验数据每条连接最多只能压满 7MByte(不同的环境可能不一样，供参考)，理论上 1 个服务提供者需要 20 个服务消费者才能压满网卡。

#### 为什么不能传大包?

因 dubbo 协议采用单一长连接，如果每次请求的数据包大小为 500KByte，假设网络为千兆网卡 [3](https://dubbo.apache.org/zh/docs/v2.7/user/references/protocol/dubbo/#fn:3)，每条连接最大 7MByte(不同的环境可能不一样，供参考)，单个服务提供者的 TPS(每秒处理事务数)最大为：128MByte / 500KByte = 262。单个消费者调用单个服务提供者的 TPS(每秒处理事务数)最大为：7MByte / 500KByte = 14。如果能接受，可以考虑使用，否则网络将成为瓶颈。

#### 为什么采用异步单一长连接?

因为服务的现状大都是服务提供者少，通常只有几台机器，而服务的消费者多，可能整个网站都在访问该服务，比如 Morgan 的提供者只有 6 台提供者，却有上百台消费者，每天有 1.5 亿次调用，如果采用常规的 hessian 服务，服务提供者很容易就被压跨，通过单一连接，保证单一消费者不会压死提供者，长连接，减少连接握手验证等，并使用异步 IO，复用线程池，防止 C10K 问题。





### 1.Dubbo线程模型

参考文档(https://zhuanlan.zhihu.com/p/157354148)



Dubbo默认的底层网络通信使用的是Netty，服务提供方NettyServer使用两级线程池，

其中`EventLoopGroup（boss）`主要用来接收客户端的链接请求，并把完成TCP三次握手的连接分发给`EventLoopGroup（worker）`来进行后续处理， 注意把**boss和worker线程组称为I/O线程**，前者处理IO连接事件，后者处理IO读写事件。



除了I/O 线程外，还有用于业务处理的业务线程。Dubbo Provider如何使用这些线程呢？

- 如果处理逻辑较为简单，并且不会发起新的I/O请求，那么直接在I/O线程上处理会更快，因为这样减少了线程池调度与上下文切换的开销，毕竟线程切换还是有一定成本的。
- 如果逻辑较为复杂，或者需要发起网络通信，比如查询数据库，则I/O线程必须派发请求到新的线程池进行处理，否则I/O线程会被阻塞，导致处理IO请求效率降低。



Dubbo中根据请求的消息类是直接被I/O线程处理还是被业务线程池处理，Dubbo提供了下面几种线程模型：

![image-20210521145911045](D:\Users\80233448\AppData\Roaming\Typora\typora-user-images\image-20210521145911045.png)

- **all（AllDispatcher类）**：所有消息都派发到业务线程池，这些消息包括请求、响应、连接事件、断开事件等，响应消息会优先使用对于请求所使用的线程池。(默认选择这个)
- **direct（DirectDispatcher类）**：所有消息都不派发到业务线程池，全部在IO线程上直接执行。
- **message（MessageOnlyDispatcher类）**：只有请求响应消息派发到业务线程池，其他消息如连接事件、断开事件、心跳事件等，直接在I/O线程上执行。
- **execution（ExecutionDispatcher类）**：只把请求类消息派发到业务线程池处理，但是响应、连接事件、断开事件、心跳事件等消息直接在I/O线程上执行。
- **connection（ConnectionOrderedDispatcher类）**：在I/O线程上将连接事件、断开事件放入队列，有序地逐个执行，其他消息派发到业务线程池处理。



//todo 上面这些类型的区别和优缺点、适用场景

> 那Dubbo默认的线程模型是哪种呢？

从netty启动流程来看，初始化NettyServer时会进行加载具体的线程模型，代码如下：

```java
public NettyServer(URL url, ChannelHandler handler) throws RemotingException {
    super(ExecutorUtil.setThreadName(url, SERVER_THREAD_POOL_NAME), ChannelHandlers.wrap(handler, url));
}
public static ChannelHandler wrap(ChannelHandler handler, URL url) {
    return ChannelHandlers.getInstance().wrapInternal(handler, url);
}
protected ChannelHandler wrapInternal(ChannelHandler handler, URL url) {
    return new MultiMessageHandler(new HeartbeatHandler(ExtensionLoader.getExtensionLoader(Dispatcher.class)
            .getAdaptiveExtension().dispatch(handler, url)));
}
```

这里根据URL里的线程模型来选择具体的Dispatcher实现类。

Dubbo提供的Dispatcher类，其默认的实现类是all ，也就是AllDispatcher类。

不过Dispatcher是通过SPI方式加载的，也就是用户可以自定义自己的线程模型，只需实现Dispatcher类然后配置选择使用自定义的Dispatcher类即可。