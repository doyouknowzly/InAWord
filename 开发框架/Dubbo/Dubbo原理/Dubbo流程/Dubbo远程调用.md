## Dubbo远程调用

![/dev-guide/images/dubbo_rpc_refer.jpg](https://dubbo.apache.org/imgs/dev/dubbo_rpc_refer.jpg)

上图是服务消费的主过程：

首先 `ReferenceConfig` 类的 `init` 方法调用 `Protocol` 的 `refer` 方法生成 `Invoker` 实例(如上图中的红色部分)，这是服务消费的关键。接下来把 `Invoker` 转换为客户端需要的接口(如：HelloWorld)。



### 引用服务时序

![/dev-guide/images/dubbo-refer.jpg](https://dubbo.apache.org/imgs/dev/dubbo-refer.jpg)