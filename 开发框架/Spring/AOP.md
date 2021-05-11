## AOP

参考文档[<<AOP 面试造火箭事件始末>>](https://mp.weixin.qq.com/s/NXZp8a3n-ssnC6Y1Hy9lzw)

| 序号 | 问题          | 一句话总结                                                   |
| ---- | ------------- | ------------------------------------------------------------ |
| 0    | AOP的作用     |                                                              |
| 1    | AOP的使用场景 | 日志管理、缓存控制、权限控制 等                              |
| 2    |               |                                                              |
| 3    | AOP的术语     | **1.Join point（连接点）**： 程序执行过程中的一个点，可以被增强的点<br>**2.Pointcut（切入点）**：切入点是与连接点匹配的表达式<br>**3.Advice（增强）**：拦截到`Joinpoint`(连接点)之后所要做的事情就是增强<br>**4.Aspect（切面）**：`Aspect`切面表示`Pointcut`（切入点）和`Advice`（增强/通知）的结合 |
| 4    | AOP的常用注解 | @Before  @After  @AfterThrowing  @AfterReturning  @Around    |
| 5    | AOP的实现方式 | 对于实现了接口的类对象，Spring会使用**JDK Proxy**，去创建代理对象<br/>对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候Spring AOP会使用**Cglib**<br/>当然也可以使用 AspectJ ,Spring AOP 已经集成了AspectJ<br> |
| 6    | AspectJ的细节 | **Spring AOP 属于运行时增强，而 AspectJ 是编译时增强**<br>如果我们的切面比较少，那么两者性能差异不大。<br/>但是，当切面太多的话，最好选择 AspectJ ，它比Spring AOP 快很多。 |
|      |               |                                                              |



###  6. AspectJ的细节

