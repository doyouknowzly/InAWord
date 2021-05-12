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
|      |                  |                                                              |

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

| 序号 | 问题          | 一句话解释                                                   |
| ---- | ------------- | ------------------------------------------------------------ |
| 0    | AOP的实现方式 | 1.  JDK <br>2.  Cglib <br/>3.  AspectJ                       |
| 1    | AspectJ的原理 | **Spring AOP 属于运行时增强，而 AspectJ 是编译时增强**<br/>如果我们的切面比较少，那么两者性能差异不大。<br/>但是，当切面太多的话，最好选择 AspectJ ，它比Spring AOP 快很多。 |
|      |               |                                                              |

### 0. AOP的实现方式

对于Aop的实现，其实核心就是【如何增强】，思路也很容易想到: 【使用代理】

> 静态代理
>
> 动态代理

| 实现方式 | 代理方式 | 优点 | 缺点              | 使用时机 |
| -------- | -------- | ---- | ----------------- | -------- |
| JDK      | 静态     |      | 必须实现interface |          |
| Cglib    | 动态     |      |                   |          |
| AspectJ  | 静态     |      |                   |          |



如果使用Spring AOP，对于实现了接口的类对象，Spring会使用**JDK Proxy**，去创建代理对象<br/>对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候Spring AOP会使用**Cglib**<br/>

当然也可以使用 AspectJ ,Spring AOP 已经集成了AspectJ<br/>

###  1. AspectJ的细节

