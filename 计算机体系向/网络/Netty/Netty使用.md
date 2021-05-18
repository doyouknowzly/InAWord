## Netty使用



| 序号 | 问题                  | 一句话简介 |
| ---- | --------------------- | ---------- |
| 0    | Netty服务端的启动过程 |            |
| 1    | Netty客户端的启动过程 |            |
| 2    | Netty支持WebSocket    |            |
| 3    | Netty单机的性能范围   |            |



### 0. Netty服务端的启动过程

```java

```

1. 创建两个 `NioEventLoopGroup` 对象实例：`bossGroup` 和 `workerGroup`

   - bossGroup: 

     用于处理客户端的 TCP 连接请求 

   - workerGroup: 

     负责每一条连接的具体读写数据的处理逻辑，真正负责 I/O 读写操作，交由对应的 Handler 处理

   - 一般情况下我们会指定 bossGroup 的 线程数为 1（并发连接量不大的时候） ，workGroup 的线程数量为 **CPU 核心数 \*2** (无参构造器默认值也是2)

2. 创建了一个服务端启动引导/辅助类：`ServerBootstrap`，这个类将引导我们进行服务端的启动工作。

3. 给这个引导类注入相关的配置， 使用的是Builder模式

   - 通过.group()配置1的线程组，确定线程模型
   - 通过.channel()指定IO模型，一般使用NIO (当然，你想的话也可以使用BIO)
     - `NioServerSocketChannel` ：指定服务端的 IO 模型为 NIO，与 BIO 编程模型中的`ServerSocket`对应
     - `NioSocketChannel` : 指定客户端的 IO 模型为 NIO， 与 BIO 编程模型中的`Socket`对应
   - 通过 `.childHandler()`给引导类创建一个`ChannelInitializer` ，然后指定了服务端消息的业务处理逻辑 的`Handler` 对象

4. 调用 `ServerBootstrap` 类的 `bind()`方法绑定端口