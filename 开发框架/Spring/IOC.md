---
typora-root-url: ..\..\resource\img
---

## IOC





## Spring Bean

| 序号 | 问题                     | 一句话描述                                                   |
| ---- | ------------------------ | ------------------------------------------------------------ |
| 0    | bean的作用域             | singleton : 唯⼀ bean 实例，Spring 中的 bean 默认都是单例的。 <br>prototype : 每次请求都会创建⼀个新的 bean 实例。 <br/>request : 每⼀次HTTP请求都会产⽣⼀个新的bean，该bean仅在当前HTTP request内有效。  <br/>session : 每⼀次HTTP请求都会产⽣⼀个新的 bean，该bean仅在当前 HTTP session 内有效。  <br/>global-session： 全局session作⽤域<br><br>默认的是：单例 singleton |
| 1    | 单例模式如何保证线程安全 | 只要有成员变量，就不是线程安全的。<br>如果有线程安全的诉求，可以将变量定义为ThreadLocal 的 |
| 2    |                          |                                                              |
| 3    | bean的生命周期           | **只有四个！**<br>**实例化 -> 属性赋值 -> 初始化 -> 销毁**<br>详见 [Bean的生命周期.md](./Bean的生命周期.md) |
| 4    | bean的常用扩展点         | 各种Aware接口， initializingBean,  DisposableBean            |
| 5    | BeanFactory和FactoryBean | BeanFactory 是IOC容器<br>FactoryBean是可以创建一类Bean的工厂性质的Bean |
| 6    |                          |                                                              |
| 7    |                          |                                                              |



### 1.bean的作用域(scope)

| 作用域 | 字符      | 描述                     |
| ------ | --------- | ------------------------ |
| 单例   | singleton | 整个应用中只创建一个实例 |
| 原型   | prototype | 每次注入时都新建一个实例 |
| 会话   | session   | 为每个会话创建一个实例   |
| 请求   | request   | 为每个请求创建一个实例   |



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

### 5.BeanFactory和FactoryBean

- BeanFactory是接口，**是spring中比较原始的IOC容器**, 无法支持spring的许多插件，如AOP功能、Web应用等。

而**ApplicationContext接口，它由BeanFactory接口派生而来。**日常使用基本只使用ApplicationContext了

- FactoryBean也是接口，但本质是个Bean, 是能创建一类Bean的工厂性质的Bean。为IOC容器中Bean的实现提供了更加灵活的方式, 
  1. FactoryBean在IOC容器的基础上给Bean的实现加上了一个简单工厂模式和装饰模式
  2. **一个Bean A如果实现了FactoryBean接口，那么A就变成了一个工厂**
  3. **根据A的名称获取到的实际上是工厂调用`getObject()`返回的对象，而不是A本身，如果要获取工厂A自身的实例，那么需要在名称前面加上'`&`'符号。**

```java
@RunWith(SpringRunner.class)
@SpringBootTest(classes = TestApplication.class)
public class FactoryBeanTest {
    @Autowired
    private ApplicationContext context;
    @Test
    public void test() {
        MyBean myBean1 = (MyBean) context.getBean("myBean");
        System.out.println("myBean1 = " + myBean1.getMessage());
        MyBean myBean2 = (MyBean) context.getBean("&myBean");
        System.out.println("myBean2 = " + myBean2.getMessage());
        System.out.println("myBean1.equals(myBean2) = " + myBean1.equals(myBean2));
    }
}

```

```java
myBean1 = 通过FactoryBean.getObject()初始化实例
myBean2 = 通过构造方法初始化实例
myBean1.equals(myBean2) = false

```

