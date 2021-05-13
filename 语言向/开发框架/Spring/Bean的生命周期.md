---
typora-root-url: ..\..\resource\img
---



### bean的生命周期

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



### 3.自己总结的表格

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
| 三   |        |          | *初始化 (Initialization)*                                | AbstractAutowireCapableBeanFactory  | initializeBean()                                |                                                              |
|      | 1      |          | **通知AwareMethods**                                     |                                     | invokeAwareMethods()                            |                                                              |
|      |        | 1.1      |                                                          | BeanNameAware                       | setBeanName()                                   |                                                              |
|      |        | 1.2      |                                                          | BeanClassLoaderAware                | setBeanClassLoader()                            |                                                              |
|      |        | 1.3      |                                                          | BeanFactoryAware                    | setBeanFactory()                                |                                                              |
|      | 2      |          | **初始化前处理**                                         |                                     | applyBeanPostProcessorsBeforeInitialization()   |                                                              |
|      |        | 2.1      |                                                          | BeanPostProcessor                   | postProcessBeforeInitialization()               |                                                              |
|      | 3      |          | **初始化方法**                                           |                                     | invokeInitMethods()                             |                                                              |
|      |        | 3.1      |                                                          |                                     | @PostConstruct                                  |                                                              |
|      |        | 3.2      |                                                          | initializingBean                    | afterpropertiesSet()                            |                                                              |
|      |        | 3.3      |                                                          | \<bean>标签                         | \<init-method>方法                              |                                                              |
|      | 4      |          | **初始化后处理**                                         |                                     | applyBeanPostProcessorsAfterInitialization()    |                                                              |
|      |        | 4.1      |                                                          | BeanPostProcessor                   | postProcessorAfterInitialization()              |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |
| 四   |        |          | *销毁*                                                   | ConfigurableApplicationContext      | close()                                         |                                                              |
|      |        |          |                                                          |                                     |                                                 |                                                              |



> 流程图 processon版本可见 <<https://www.processon.com/diagraming/6099558a07912943913523c1>>

![本地版本如下](.\Bean的生命周期.png)

