## 过滤器Filter



参考文档: (https://zhuanlan.zhihu.com/p/87075739)

官方文档: (https://dubbo.apache.org/zh/docs/v2.7/dev/impls/filter/)



`Filter`是Dubbo中使用较为频繁的组件，其作用在于对所指定的请求进行过滤，功能非常类似于AOP，可以实现诸如请求过滤器和全局异常捕获器等组件。

>  每次远程方法执行，该拦截都会被执行，请注意对性能的影响。

### 一、定义

对于`Filter`的划分，

根据其面向的对象不同，可以分为service端和consumer端；

根据其所作用的范围的不同，则可以分为单个服务过滤器（单个service或reference）和全局过滤器（整个provider或consumer）。



`Filter`的指定方式主要有三种：

- 在\或\标签中使用`filter`属性来指定具体的filter名称，这种使用方式的作用级别只针对于所指定的某个provider或consumer；
- 在\或\标签中使用`filter`属性来指定具体的filter名称，这种使用方式的作用级别针对于所有的provider或consumer；
- 在所声明的实现了`Filter`接口的类上使用`@Activate`注解来标注，并且注解中的`group`属性指定为`provider`或`consumer`。



约定：

- 用户自定义 filter 默认在内置 filter 之后。
- 特殊值 `default`，表示缺省扩展点插入的位置。比如：`filter="xxx,default,yyy"`，表示 `xxx` 在缺省 filter 之前，`yyy` 在缺省 filter 之后。
- 特殊符号 `-`，表示剔除。比如：`filter="-foo1"`，剔除添加缺省扩展点 `foo1`。比如：`filter="-default"`，剔除添加所有缺省扩展点。
- provider 和 service 同时配置的 filter 时，累加所有 filter，而不是覆盖。比如：`<dubbo:provider filter="xxx,yyy"/>` 和 `<dubbo:service filter="aaa,bbb" />`，则 `xxx`,`yyy`,`aaa`,`bbb` 均会生效。如果要覆盖，需配置：`<dubbo:service filter="-xxx,-yyy,aaa,bbb" />`

### 二、用法

1. 编写: 

   编写具体代码，实现Filter

2. 声明:

   在`META-INF/dubbo`目录下新建一个名称为`org.apache.dubbo.rpc.Filter`的文件， 然后指定K-V对，例如:

   ```properties
   exceptionResolver=org.apache.dubbo.demo.example.eg4.ExceptionResolver
   ```

   Dubbo会将文件内容以键值对的形式保存下来。

   通过这种方式，Dubbo就实现了将数据的加载过程与用户使用的过程进行解耦

3. 指定:

   在dubbo.consumer或dubbo.provider配置文件里进行指定 

   ```xml
   <!-- 这种方式只会针对DemoService这一个服务提供者使用该过滤器 -->
   <dubbo:service interface="org.apache.dubbo.demo.example.eg4.DemoService" ref="demoService" filter="exceptionResolver"/>
   <!-- 这种方式会针对所有的provider服务提供者使用该过滤器 -->
   <dubbo:provider filter="exceptionResolver"/>
   ```

   `filter`属性的值是在前面配置文件中所使用的键名

   

   or 在Filter的实现类上使用@Activate注解

   ```java
   // 这种方式主要用在Filter实现类上，group属性表示当前类会针对所有的provider所使用
   @Activate(group = Constants.PROVIDER)
   ```

   `group`字段表示该实现类所属的一个分组，这里是provider端.

   > 一般使用provider、consumer也就够了，这时会分别给两端的invoker都增加当前的Filter
   >
   > 但是也可以使用自定义的全路径类名，比如

   在resources下新建META-INF/dubbo/internal文件夹， 新建文件，名字是自定义Filter的全路径名，在配置文件中可以这样配:

   ```properties
   group1 = com.alibaba.dubbo.demo.provider.activate.impl.GroupActivateExtImpl
   ```

   使用的时候就

   ```java
   @Activiate( group = "group1" )
   public class FilterA implements Filter {
       
   }
   ```

   

### 三、原理

在Dubbo中，对于服务的调用，最终是将其抽象为一个`Invoker`进行的，而在抽象的过程中，Dubbo会获取配置文件中指定的所有实现了`Filter`接口的类，然后根据为其指定的key名称，将其组织成一条链。

<img src="https://pic3.zhimg.com/80/v2-2d1aa9595ec88199fd76221cb8467d96_720w.jpg" alt="img" style="zoom:67%;" />

通过上面的图可以看出，Dubbo过滤器的整个调用过程都是通过`Invoker`驱动的，最终对外的表现就是一个`Invoker`的头结点对象，通过这种方式，Dubbo能够将整个调用过程都统一化到一个`Invoker`对象中。



具体的代码在`ProtocolFilterWrapper`中， 核心代码如下：

```java
private static <T> Invoker<T> buildInvokerChain(final Invoker<T> invoker, 
        String key, String group) {
    Invoker<T> last = invoker;
    // 获取所有实现了Filter接口的子类，这里key是service.filter，也就是说，其对应的配置位置在
    // <dubbo:service/>标签的filter属性中。group是provider，这个参数指明了这些Filter中
    // 只有provider类型的Filter才会在这里被组装进来。
    // 从整体上看，如果在配置文件中通过filter属性指定了各个filter的名称，那么这里就会通过SPI
    // 读取指定文件中的Filter实现子类，然后取其中的provider组内的Filter将其返回，以便进行后续的组装
    List<Filter> filters = ExtensionLoader.getExtensionLoader(Filter.class)
      .getActivateExtension(invoker.getUrl(), key, group);
    if (!filters.isEmpty()) {
      // 这里的整个动作其实就是对链的一个组装，比如通过上面的步骤获取到了三个Filter：A、B和C。
      // 在这里会为每一个子类都声明一个Invoker对象，将该对象的invoke()方法委托给链的下一个节点。
      // 这样，通过不断的委托动作，在遍历完成之后，就会得到一个Invoker的头结点，最后将头结点返回。
      // 这样就达到了组装Invoker链的目的
      for (int i = filters.size() - 1; i >= 0; i--) {
        final Filter filter = filters.get(i);
        final Invoker<T> next = last;
        last = new Invoker<T>() {

          @Override
          public Class<T> getInterface() {
            return invoker.getInterface();
          }

          @Override
          public URL getUrl() {
            return invoker.getUrl();
          }

          @Override
          public boolean isAvailable() {
            return invoker.isAvailable();
          }

          @Override
          public Result invoke(Invocation invocation) throws RpcException {
            // filter指向的是当前节点，而传入的Invoker参数是其下一个节点
            Result result = filter.invoke(next, invocation);
            if (result instanceof AsyncRpcResult) {
              AsyncRpcResult asyncResult = (AsyncRpcResult) result;
              asyncResult.thenApplyWithContext(r -> 
                  filter.onResponse(r, invoker, invocation));
              return asyncResult;
            } else {
              return filter.onResponse(result, invoker, invocation);
            }
          }

          @Override
          public void destroy() {
            invoker.destroy();
          }

          @Override
          public String toString() {
            return invoker.toString();
          }
        };
      }
    }
```



