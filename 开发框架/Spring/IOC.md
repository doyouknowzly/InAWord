## IOC





## Spring Bean

| 序号 | 问题                     | 一句话描述                                                   |
| ---- | ------------------------ | ------------------------------------------------------------ |
| 0    | bean的作用域             | singleton : 唯⼀ bean 实例，Spring 中的 bean 默认都是单例的。 <br>prototype : 每次请求都会创建⼀个新的 bean 实例。 <br/>request : 每⼀次HTTP请求都会产⽣⼀个新的bean，该bean仅在当前HTTP request内有效。  <br/>session : 每⼀次HTTP请求都会产⽣⼀个新的 bean，该bean仅在当前 HTTP session 内有效。  <br/>global-session： 全局session作⽤域 |
| 1    | 单例模式如何保证线程安全 | 使用ThreadLocal                                              |
| 2    |                          |                                                              |
| 3    | bean的生命周期           | **只有四个！**<br>**实例化 -> 属性赋值 -> 初始化 -> 销毁**<br> |
| 4    | bean的常用扩展点         | 各种Aware接口， initializingBean,  DisposableBean            |
| 5    | BeanFactory和FactoryBean |                                                              |
| 6    |                          |                                                              |
| 7    |                          |                                                              |
| 8    |                          |                                                              |



### 3. bean的生命周期

参考文档[<<Spring Bean的生命周期（非常详细）>>](https://www.cnblogs.com/zrtqsk/p/3735273.html)



1. 流程图

![img](https://images0.cnblogs.com/i/580631/201405/181453414212066.png)

![img](https://images0.cnblogs.com/i/580631/201405/181454040628981.png)

2. 流程总结: 

   分四部分 - 实例化 Instantiation 属性赋值 Populate 初始化 Initialization 销毁 Destruction

   **实例化 -> 属性赋值 -> 初始化 -> 销毁**

   主要逻辑都在AbstractAutoWiredCapableBeanFactory.doCreate()方法中，

   逻辑很清晰，就是顺序调用以下三个方法，这三个方法与三个生命周期阶段一一对应，非常重要，在后续扩展接口分析中也会涉及。

   1.  createBeanInstance() -> 实例化
   2.  populateBean() -> 属性赋值
   3.  initializeBean() -> 初始化

   至于销毁，是在容器关闭时调用的，详见`ConfigurableApplicationContext#close()`



### 自己总结的表格

| 顺序 | 子顺序 | 三级顺序 | 大流程                                                   | 类                                  | 方法                                            | 备注                                                         |
| ---- | ------ | -------- | -------------------------------------------------------- | ----------------------------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| 零   |        |          | *准备BeanDefination*                                     |                                     |                                                 |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |
|      |        |          | 创建Bean                                                 |                                     | doCreateBean()                                  |                                                              |
| 一   |        |          | *实例化 (Instantiation)*                                 | AbstractAutowireCapableBeanFactory  | createBeanInstance()                            |                                                              |
|      | 1      |          | 非反射实例化                                             | InstanceSupplier                    | obtainFromSupplier()                            | java8提供的函数式方法，在实例化的时候，不需要反射，直接调用AbstractBeandefinition中的这个构造器 |
|      | 2      |          | 使用工厂方法实例化                                       | BeanFactory                         | instantiateUsingFactoryMethod()                 |                                                              |
|      | 3      |          | 自动注入构造器<br>(@AutoWired写在构造方法上，不是属性上) |                                     | autowireConstructor()                           |                                                              |
|      | 4      |          | 无参构造器                                               |                                     | instantiateBean()  <br>[就是简单调用无参构造器] |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |
| 二   |        |          | *属性赋值*                                               | AbstractAutowireCapableBeanFactory  | populateBean()                                  |                                                              |
|      | 1      |          | **实例化后处理**                                         | InstantiationAwareBeanPostProcessor | postProcessAfterInstantiatio()                  |                                                              |
|      | 2      |          | **自动装填**                                             |                                     | autowireByName()\autowireByType()               |                                                              |
|      | 3      |          | 赋值后置处理                                             | InstantiationAwareBeanPostProcessor | postProcessProperties()                         |                                                              |
|      | 4      |          | **已弃用**被上面这个替代了                               | InstantiationAwareBeanPostProcessor | postProcessPropertyValues()                     |                                                              |
|      |        |          |                                                          |                                     | applyPropertyValues()                           |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |
| 三   |        |          | *实例化 (Initialization)*                                | AbstractAutowireCapableBeanFactory  | initializeBean()                                |                                                              |
|      | 1      |          | **通知AwareMethods**                                     |                                     | invokeAwareMethods()                            |                                                              |
|      |        | 1.1      |                                                          | BeanNameAware                       | setBeanName()                                   |                                                              |
|      |        | 1.2      |                                                          | BeanClassLoaderAware                | setBeanClassLoader()                            |                                                              |
|      |        | 1.3      |                                                          | BeanFactoryAware                    | setBeanFactory()                                |                                                              |
|      | 2      |          | **初始化前处理**                                         |                                     | applyBeanPostProcessorsBeforeInitialization()   |                                                              |
|      |        | 2.1      |                                                          | BeanPostProcessor                   | postProcessBeforeInitialization()               |                                                              |
|      | 3      |          | **初始化方法**                                           |                                     | invokeInitMethods()                             |                                                              |
|      |        | 3.1      |                                                          | initializingBean                    | afterpropertiesSet()                            |                                                              |
|      |        | 3.2      |                                                          | \<bean>标签                         | \<init-method>方法                              |                                                              |
|      | 4      |          | **初始化后处理**                                         |                                     | applyBeanPostProcessorsAfterInitialization()    |                                                              |
|      |        | 4.1      |                                                          | BeanPostProcessor                   | postProcessorAfterInitialization()              |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |
| 四   |        |          | *销毁*                                                   | ConfigurableApplicationContext      | close()                                         |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |



### 4. bean的常用扩展点

参考文档： 																																																																																																																																																																																																																																																																																																																																																																																						[请别再问Spring Bean的生命周期了！](https://www.jianshu.com/p/1dec08d290c1)



> 注意两个单词
>
> | 单词           | 含义                         |
> | -------------- | ---------------------------- |
> | Instantiation  | 表示**实例化**, 对象还未生成 |
> | Initialization | 表示**初始化**, 对象已经生成 |

- #### 第一大类：影响多个Bean的接口

  实现了这些接口的Bean会切入到多个Bean的生命周期中。

  正因为如此，这些接口的功能非常强大，Spring内部扩展也经常使用这些接口，例如自动注入以及AOP的实现都和他们有关。

  - BeanPostProcessor

  - InstantiationAwareBeanPostProcessor

    - InstantiationAwareBeanPostProcessor实际上继承了BeanPostProcessor接口，严格意义上来看他们不是两兄弟，而是两父子。

    <img src="https://upload-images.jianshu.io/upload_images/4558491-dc3eebbd1d6c65f4.png?imageMogr2/auto-orient/strip|imageView2/2/w/823/format/webp" alt="img" style="zoom: 80%;" />

- #### 第二大类：只调用一次的接口

  特点是只能影响自己，常用于用户自定义扩展， 又可以分为两类：

  - Aware类型的接口
    - 作用就是让我们能够拿到Spring容器中的一些资源
    - 调用时机需要注意：所有的Aware方法都是在初始化阶段之前调用的！

  - 生命周期接口
  
    - InitializingBean , 对应生命周期的初始化阶段
  
    > 因为Aware方法都是执行在初始化方法之前，所以可以在初始化方法中放心地使用Aware接口获取的资源，这也是我们自定义扩展Spring的常用方式
  
    - DisposableBean, 对应生命周期的销毁阶段