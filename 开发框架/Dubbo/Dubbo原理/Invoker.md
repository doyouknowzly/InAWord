# Invoker

由于 `Invoker` 是 Dubbo 领域模型中非常重要的一个概念，很多设计思路都是向它靠拢。这就使得 `Invoker` 渗透在整个实现代码里，对于刚开始接触 Dubbo 的人，确实容易给搞混了。 

下面我们用一个精简的图来说明最重要的两种 `Invoker`：

服务提供 `Invoker`   和  服务消费 `Invoker`：

![/dev-guide/images/dubbo_rpc_invoke.jpg](https://dubbo.apache.org/imgs/dev/dubbo_rpc_invoke.jpg)

provider的实现类被封装成为一个 `AbstractProxyInvoker` 实例，并新生成一个 `Exporter` 实例。

这样当网络通讯层收到一个请求后，会找到对应的 `Exporter` 实例，并调用它所对应的 `AbstractProxyInvoker` 实例，从而真正调用了服务提供者的代码



consumer在调用rpc时，注入的bean其实就是上图的proxy, 用户代码通过这个 proxy 调用其对应的 `Invoker`，而该 `Invoker` 实现了真正的远程服务调用。

