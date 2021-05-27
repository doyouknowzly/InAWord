## Adaptive注解

参考文档 (https://zhuanlan.zhihu.com/p/87075689)

官方文档(https://dubbo.apache.org/zh/docs/v2.7/dev/spi/)



### 一、概览

Dubbo提供了一种SPI的机制用于动态的加载扩展类，但是如何在运行时动态的选用哪一种扩展类来提供服务，这就需要一种机制来进行动态的匹配。

Dubbo SPI中提供的Adaptive机制就为解决这个问题提供了一种良好的解决方案



对应于Adaptive机制，Dubbo提供了一个注解`@Adaptive`，该注解可以用于接口的某个子类上，也可以用于接口方法上。

- 如果用在接口的子类上，则表示Adaptive机制的实现会按照该子类的方式进行自定义实现；

  - 这种方式， Dubbo里只有`ExtensionFactory`接口使用了， 其有一个子类`AdaptiveExtensionFactory`就使用了`@Adaptive`注解进行了标注。

    主要作用就是在获取目标对象时，分别通过`ExtensionLoader`和`Spring容器`两种方式获取

- 如果用在方法上，则表示Dubbo会为该接口自动生成一个子类，并且按照一定的格式重写该方法。

- 而其余没有标注`@Adaptive`注解的方法将会默认抛出异常。



### 二、使用

一般是这样使用: 

@SPI 后的值是默认值， 如果使用ExtensionLoader时，没有指定使用哪个实现类来提供服务，默认使用括号里这个

```java
@SPI("apple")
public interface FruitGranter {

  Fruit grant();

  @Adaptive
  //@Adaptive("apple")
  String watering(URL url);
}
```





我们主要要注意如下几个问题：

- 所有未使用`@Adaptive`注解标注的接口方法，默认都会抛出异常；
- 在使用`@Adaptive`注解标注的方法中，其参数中必须有一个参数类型为URL，或者其某个参数提供了某个方法，该方法可以返回一个URL对象；
- 在方法的实现中会通过URL对象获取某个参数对应的参数值，如果在接口的`@SPI`注解中指定了默认值，那么在使用URL对象获取参数值时，如果没有取到，就会使用该默认值；
- 最后根据获取到的参数值，在`ExtensionLoader`中获取该参数值对应的服务提供类对象，然后将真正的调用委托给该服务提供类对象进行；
- 在通过URL对象获取参数时，参数key获取的对应规则是，首先会从`@Adaptive`注解的参数值中获取，如果该注解没有指定参数名，那么就会默认将目标接口的类名转换为点分形式作为参数名，比如这里`FruitGranter`转换为点分形式就是`fruit.granter`。





### 三、原理

主要分为如下三个步骤：

- 加载标注有`@Adaptive`注解的接口，如果不存在，则不支持Adaptive机制；
- 为目标接口按照一定的模板生成子类代码，并且编译生成的代码，然后通过反射生成该类的对象；
- 结合生成的对象实例，通过传入的URL对象，获取指定key的配置，然后加载该key对应的类对象，最终将调用委托给该类对象进行。
