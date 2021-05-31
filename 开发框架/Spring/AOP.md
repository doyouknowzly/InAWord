## AOP的使用

参考文档[<<AOP 面试造火箭事件始末>>](https://mp.weixin.qq.com/s/NXZp8a3n-ssnC6Y1Hy9lzw)

| 序号 | 问题             | 一句话总结                                                   |
| ---- | ---------------- | ------------------------------------------------------------ |
| 1    | AOP的使用场景    | 日志管理、缓存控制、权限控制 等                              |
| 2    | AOP的术语        | **1.Join point（连接点）**： 程序执行过程中的一个点，可以被增强的点<br/>**2.Pointcut（切入点）**：切入点是与连接点匹配的表达式<br/>**3.Advice（增强）**：拦截到`Joinpoint`(连接点)之后所要做的事情就是增强<br/>**4.Aspect（切面）**：`Aspect`切面表示`Pointcut`（切入点）和`Advice`（增强/通知）的结合 |
| 3    | 增强的执行顺序   |                                                              |
| 4    | AOP的常用注解    | @Before  @After  @AfterThrowing  @AfterReturning  @Around    |
| 5    | execution 表达式 | ***execution(<修饰符模式>?<返回类型模式><方法名模式>(<参数模式>)<异常模式>?)*** |
| 6    | AOP的示例代码    | 参考 [异常处理AOP](../../utils/轮子代码/java/ErrorCatchAop.md) |

### 3. 增强的执行顺序

1. 正常情况

   ![img](https://upload-images.jianshu.io/upload_images/12170632-2931198a9b094f45.jpeg?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

2. 多个切面情况， 可以通过@Order指定先后顺序，数字越小，优先级越高。

   ![img](https://upload-images.jianshu.io/upload_images/12170632-67b89b71dc0cb8ac.jpeg?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)





### 5.execution 表达式

对于 execution 表达式，官网对 execution 表达式的介绍为：

***execution(<修饰符模式>?<返回类型模式><方法名模式>(<参数模式>)<异常模式>?)***

除了返回类型模式、方法名模式和参数模式外，其它项都是可选的。这个解释可能有点难理解，下面我们通过一个具体的例子来了解一下。在 HandleResultAspect 中我们定义了一个切点，其 execution 表达式为：`* com.study.spring.controller..*.*(..))`，下表为该表达式比较通俗的解析：

| **标识符**                    | **含义**                                                     |
| ----------------------------- | ------------------------------------------------------------ |
| `execution（）`               | 表达式的主体                                                 |
| 第一个 `*` 符号               | 表示返回值的类型，`*` 代表所有返回类型                       |
| `com.study.spring.controller` | AOP 所切的服务的包名，即需要进行横切的业务类                 |
| 包名后面的 `..`               | 表示当前包及子包                                             |
| 第二个 `*`                    | 表示类名，`*` 表示所有类                                     |
| 最后的 `.*(..)`               | 第一个 `.` 表示任何方法名，括号内为参数类型，`..` 代表任何类型参数 |













## AOP的原理

| 序号 | 问题               | 一句话解释                                                   |
| ---- | ------------------ | ------------------------------------------------------------ |
| 0    | 静态代理和动态代理 |                                                              |
| 1    | AOP的实现方式      | 1.  JDK  <br>使用 Proxy 来创建代理类，增强逻辑写在 InvocationHandler.invoke() 里<br>2.  Cglib <br/>提供了类似的  Enhancer 类，增强逻辑写在 MethodInterceptor.intercept() 中 <br>3.  AspectJ |
| 2    | AspectJ的细节      | **Spring AOP 属于运行时增强，而 AspectJ 是编译时增强**<br/>如果我们的切面比较少，那么两者性能差异不大。<br/>但是，当切面太多的话，最好选择 AspectJ ，它比Spring AOP 快很多。 |
|      |                    |                                                              |

### 0. 静态代理和动态代理

对于Aop的实现，其实核心就是【如何增强】，思路也很容易想到: 【使用代理】

> 静态和动态的区别就在于字节码生成的时机
>
> **静态代理** ：在**程序运行前**（编译时）代理类的.class文件就已经存在了**动态代理**
>
> **动态代理** ：在**程序运行后**通过反射创建生成字节码再由 JVM 加载而成

对比如下

| 代理方式 | 优点                 | 缺点                                                         |
| -------- | -------------------- | ------------------------------------------------------------ |
| 静态     | 性能好               | 1、如果要代理多个委托类，就要写多个代理（其实1个代理类代理多个接口也行，不过不符合单一职责原则）<br>2、每个代理类都容易出现重复的代码 |
| 动态     | 避免了静态代理的缺点 | 性能略差                                                     |

### 1.AOP的实现方式

| 实现方式 | 代理方式 | 优点                                           | 缺点                       | 一句话原理                                                   |
| -------- | -------- | ---------------------------------------------- | -------------------------- | ------------------------------------------------------------ |
| JDK      | 动态     | 避免了静态代理的缺点                           | 必须实现interface          | java.lang.reflect 包下有Proxy类, Proxy 使用反射来创建代理类，增强逻辑写在 InvocationHandler.invoke() 里 |
| Cglib    | 动态     | 性能比JDK强                                    | final方法、final类不能增强 | 直接继承自委托类,  提供了类似的  Enhancer 类管理增强和代理类，增强逻辑写在 MethodInterceptor.intercept() 中 |
| AspectJ  | 静态     | 性能好, 能做Spring AOP做不了的事（修改整个类） |                            |                                                              |



如果使用Spring AOP，对于实现了接口的类对象，Spring会使用**JDK Proxy**，去创建代理对象<br/>对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候Spring AOP会使用**Cglib** ,  思路就是代理类继承目标类，**非 final 方法**都会被方法拦截器拦截，并按照编码的表达式要求，看看要不要使用增强

> CGLIB 是高效的代码生成包，底层依靠 ASM（开源的 java 字节码编辑类库）操作字节码实现的，性能比 JDK 强

**FastClass机制**

​	JDK动态代理使用反射来调用被织入的方法，由于反射的效率比较低，所以 CGlib 采用了FastClass 的机制来实现对被拦截方法的调用。FastClass 机制就是对一个类的方法建立索引，通过索引来直接调用相应的方法， 参考文档 [<<[cglib 动态代理原理分析]>>](https://www.cnblogs.com/cruze/p/3865180.html)



当然也可以使用 AspectJ ,Spring AOP 已经集成了AspectJ，使用的注解也是兼容AspectJ的，目的就是借用人家的能力，使用一样的注解降低学习成本

下面是Spring AOP 和AspectJ的对比<br/>

| Joinpoint                    | Spring AOP Supported | AspectJ Supported |
| :--------------------------- | :------------------: | :---------------: |
| Method Call                  |          No          |        Yes        |
| Method Execution             |         Yes          |        Yes        |
| Constructor Call             |          No          |        Yes        |
| Constructor Execution        |          No          |        Yes        |
| Static initializer execution |          No          |        Yes        |
| Object initialization        |          No          |        Yes        |
| Field reference              |          No          |        Yes        |
| Field assignment             |          No          |        Yes        |
| Handler execution            |          No          |        Yes        |
| Advice execution             |          No          |        Yes        |



| Spring AOP                                       | AspectJ                                                      |
| :----------------------------------------------- | :----------------------------------------------------------- |
| 在纯 Java 中实现                                 | 使用 Java 编程语言的扩展实现                                 |
| 不需要单独的编译过程                             | 除非设置 LTW，否则需要 AspectJ 编译器 (ajc)                  |
| 只能使用运行时织入                               | 运行时织入不可用。支持编译时、编译后和加载时织入             |
| 功能不强-仅支持方法级编织                        | 更强大 - 可以编织字段、方法、构造函数、静态初始值设定项、最终类/方法等......。 |
| 只能在由 Spring 容器管理的 bean 上实现           | 可以在所有域对象上实现                                       |
| 仅支持方法执行切入点                             | 支持所有切入点                                               |
| 代理是由目标对象创建的, 并且切面应用在这些代理上 | 在执行应用程序之前 (在运行时) 前, 各方面直接在代码中进行织入 |
| 比 AspectJ 慢多了                                | 更好的性能                                                   |
| 易于学习和应用                                   | 相对于 Spring AOP 来说更复杂                                 |

###  2. AspectJ的细节

AspectJ全称是Eclipse AspectJ, 可以单独使用，也可以整合到其它框架中。单独使用AspectJ时需要使用专门的编译器ajc。(java默认的编译器是javac)

在spring中使用aspectj，不需要添加aspectjrt.jar，也不需要专门的ajc编译器，使用javac编译即可。

AspectJ属于静态织入，通过修改代码来实现，有如下几个织入的时机：

1. 编译期织入(Compile-time weaving): 如类 A 使用 AspectJ 添加了一个属性，类 B 引用了它，这个场景就需要编译期的时候就进行织入，否则没法编译类 B。

2. 编译后织入(Post-compile weaving): 也就是已经生成了 .class 文件，或已经打成 jar 包了，这种情况我们需要增强处理的话，就要用到编译后织入。

3. 类加载后织入（Load-time weaving):  指的是在加载类的时候进行织入，要实现这个时期的织入，有几种常见的方法。1、自定义类加载器来干这个，这个应该是最容易想到的办法，在被织入类加载到 JVM 前去对它进行加载，这样就可以在加载的时候定义行为了。2、在 JVM 启动的时候指定 AspectJ 提供的 agent：`-javaagent:xxx/xxx/aspectjweaver.jar`。

AspectJ可以做Spring AOP干不了的事情 (比如: 修改字段、方法、构造函数、静态变量、final类、final方法等)，

它是AOP编程的完全解决方案，Spring AOP则致力于解决企业级开发中最普遍的AOP（方法织入）。而不是成为像AspectJ一样的AOP方案