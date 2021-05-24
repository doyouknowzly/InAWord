## Dubbo扩展点



| 序号 | 问题                     | 一句话概括                                                   |
| ---- | ------------------------ | ------------------------------------------------------------ |
| 0    | SPI机制                  | Dubbo没有直接使用Java SPI， 而是做了些改动，但是兼容了Java SPI |
| 1    | Adaptive注解             | [Adaptive](./Adaptive.md)                                    |
| 2    | 过滤器Filter             | [过滤器Filter](./过滤器Filter.md)                            |
|      |                          |                                                              |
|      |                          |                                                              |
|      | 如果要做调用链，怎么实现 |                                                              |



### 0. SPI机制

Dubbo**采用微内核设计+SPI扩展**, 使得有特殊需求的接入方可以自定义扩展，做定制的二次开发。

> 什么叫 S9PI ？ SPI (Service Provider Interface)，主要是用来在框架中使用的，最常见和莫过于我们在访问数据库时候用到的`java.sql.Driver`接口了

官方文档 : 

(https://dubbo.apache.org/zh/docs/v2.7/dev/spi/) 

(https://dubbo.apache.org/zh/docs/v2.7/dev/impls/)

- Java SPI 是这样做的，约定在 Classpath 下的 META-INF/services/ 目录里创建一个**以服务接口命名的文件**，然后**文件里面记录的是此 jar 包提供的具体实现类的全限定名**。
  - 配置之后可以使用ServiceLoader进行加载，加载对应路径下文件的配置，生成接口的实现类

- 为什么Dubbo不使用Java SPI呢

  - JDK 标准的 SPI 会一次性实例化扩展点所有实现，如果有扩展实现初始化很耗时，但如果没用上也加载，会很浪费资源。
- 如果扩展点加载失败，连扩展点的名称都拿不到了。比如：JDK 标准的 ScriptEngine，通过 `getName()` 获取脚本类型的名称，但如果 RubyScriptEngine 因为所依赖的 jruby.jar 不存在，导致 RubyScriptEngine 类加载失败，这个失败原因被吃掉了，和 ruby 对应不起来，当用户执行 ruby 脚本时，会报不支持 ruby，而不是真正失败的原因。
  - 增加了对扩展点 IoC 和 AOP 的支持，一个扩展点可以直接 setter 注入其它扩展点。

- Dubbo SPI的思路？ 如何解决Java SPI的问题？

  通过指定一个名字，来定向加载；而不是全部遍历。 

  get()的时候，其实就是从Map里去取缓存

- Dubbo SPI的约定

  - META-INF/services/ 目录：该目录下的 SPI 配置文件是为了用来兼容 Java SPI 。

  - META-INF/dubbo/ 目录：该目录存放用户自定义的 SPI 配置文件。

  - META-INF/dubbo/internal/ 目录：该目录存放 Dubbo 内部使用的 SPI 配置文件。

    

- 如何使用Dubbo SPI

  - 1.在  META-INF/dubbo 目录下按接口全限定名建立一个文件

    ```properties
    children1 = com.zly.spi.Children1
    ```

    

  - 2.在接口上使用@SPI注解

  - 3.代码使用

  ```java
  public static void main(){
      //通过ExtensionLoader.getExtensionLoader获取Extentsion
      ExtensionLoader<A> ext = ExtensionLoader.getExtensionLoader(A.class);
      A children1 = ext.getExtension("children1");
      childeren1.doSomething();
  }
  ```

  





