## Netty使用



| 序号 | 问题                  | 一句话简介 |
| ---- | --------------------- | ---------- |
| 0    | Netty服务端的启动过程 |            |
| 1    | Netty客户端的启动过程 |            |
|      |                       |            |
|      |                       |            |



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

3. 给这个引导类注入相关的配置