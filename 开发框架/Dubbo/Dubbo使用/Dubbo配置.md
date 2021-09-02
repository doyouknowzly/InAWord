## Dubbo 配置



参考官方文档 

(https://dubbo.apache.org/zh/docs/v2.7/user/references/xml/) 

(https://dubbo.apache.org/zh/docs/v2.7/user/configuration/xml/)

| 序号 | 问题                   | 一句话简介                                                   |
| ---- | ---------------------- | ------------------------------------------------------------ |
| 0    | 标签分类               |                                                              |
| 1    | 标签作用               |                                                              |
| 2    | 标签间层级关系         |                                                              |
| 3    | 不同粒度配置的覆盖关系 |                                                              |
| 4    | 配置的解析             | 所有 dubbo 的标签，都统一用 `DubboBeanDefinitionParser` 进行解析，<br>基于一对一属性映射，将 XML 标签解析为 Bean 对象<br> <br>在 `ServiceConfig.export()` 或 `ReferenceConfig.get()` 初始化时，<br>将 Bean 对象转换 URL 格式，所有 Bean 属性转成 URL 的参数 |
| 5    | 本地直连               | <dubbo:reference id="userFacade" interface="com.example.modules.user.UserFacade" url="dubbo://localhost:20880?serialization=protustuff" /> |

### 0.配置分类

所有配置项分为三大类，参见下表中的"作用" 一列。

- 服务发现：表示该配置项用于服务的注册与发现，目的是让消费方找到提供方。
- 服务治理：表示该配置项用于治理服务间的关系，或为开发测试提供便利条件。
- 性能调优：表示该配置项用于调优性能，不同的选项对性能会产生影响



所有配置最终都将转换为 URL 表示，并由服务提供方生成，经注册中心传递给消费方，各属性对应 URL 的参数

- URL 格式：`protocol://username:password@host:port/path?key=value&key=value`

- 注意：只有 group，interface，version 是服务的匹配条件，三者决定是不是同一个服务，其它配置项均为调优和治理参数



### 1.配置作用

| `<dubbo:service/>`                                           | 服务配置     | 用于暴露一个服务，定义服务的元信息，一个服务可以用多个协议暴露，一个服务也可以注册到多个注册中心 |
| ------------------------------------------------------------ | ------------ | ------------------------------------------------------------ |
| `<dubbo:reference/>` [2](https://dubbo.apache.org/zh/docs/v2.7/user/configuration/xml/#fn:2) | 引用配置     | 用于创建一个远程服务代理，一个引用可以指向多个注册中心       |
| `<dubbo:protocol/>`                                          | 协议配置     | 用于配置提供服务的协议信息，协议由提供方指定，消费方被动接受 |
| `<dubbo:application/>`                                       | 应用配置     | 用于配置当前应用信息，不管该应用是提供者还是消费者           |
| `<dubbo:module/>`                                            | 模块配置     | 用于配置当前模块信息，可选                                   |
| `<dubbo:registry/>`                                          | 注册中心配置 | 用于配置连接注册中心相关信息                                 |
| `<dubbo:monitor/>`                                           | 监控中心配置 | 用于配置连接监控中心相关信息，可选                           |
| `<dubbo:provider/>`                                          | 提供方配置   | 当 ProtocolConfig 和 ServiceConfig 某属性没有配置时，采用此缺省值，可选 |
| `<dubbo:consumer/>`                                          | 消费方配置   | 当 ReferenceConfig 某属性没有配置时，采用此缺省值，可选      |
| `<dubbo:method/>`                                            | 方法配置     | 用于 ServiceConfig 和 ReferenceConfig 指定方法级的配置信息   |
| `<dubbo:argument/>`                                          | 参数配置     | 用于指定方法参数配置                                         |



### 2. 配置间层级关系

![dubbo-config](https://dubbo.apache.org/imgs/user/dubbo-config.jpg)

### 3. 不同粒度配置的覆盖关系

以 timeout 为例，下图显示了配置的查找顺序，其它 retries, loadbalance, actives 等类似：

- 方法级优先，接口级次之，全局配置再次之。
- 如果级别一样，则消费方优先，提供方次之。

其中，服务提供方配置，通过 URL 经由注册中心传递给消费方。



> 理论上 ReferenceConfig 中除了`interface`这一项，其他所有配置项都可以缺省不配置。
>
> 框架会自动使用ConsumerConfig，ServiceConfig, ProviderConfig等提供的缺省配置。

![dubbo-config-override](https://dubbo.apache.org/imgs/user/dubbo-config-override.jpg)