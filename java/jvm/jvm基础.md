## 面试题

| 序号 | 问题                                          |
| ---- | --------------------------------------------- |
| 0    | java类加载机制                                |
| 1    | 讲讲双亲委派机制                              |
| 2    | 常见的OOM问题，解决思路                       |
| 3    | 强、软、弱、虚 四种引用的定义、用法、应用场景 |

## 回答

### 0.java类加载机制

当程序主动使用某个类时，如果该类还未被加载到内存中，则JVM会通过加载、连接、初始化3个步骤来对该类进行初始化。如果没有意外，JVM将会连续完成3个步骤，所以有时也把这个3个步骤统称为类加载或类初始化。


![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e105f2913fce418bb82559efb56b2789~tplv-k3u1fbpfcp-watermark.image)

0.1 类加载时机  

- 创建类的实例，也就是new一个对象
- 访问某个类或接口的静态变量，或者对该静态变量赋值
- 调用类的静态方法
- 反射（Class.forName("com.xxx")）
- 初始化一个类的子类（会首先初始化子类的父类）
- JVM启动时标明的启动类，即文件名和类名相同的那个类    

0.2 类加载器  
类加载器基本职责就是根据类的二进制名（binary name）读取java编译器编译好的字节码文件（.class文件），并且转化生成一个java.lang.Class类的一个实例。这样的每个实例用来表示一个Java类，jvm就是用这些实例来生成java对象的。  

JVM预定义有三种类加载器，当一个 JVM启动的时候，Java开始使用如下三种类加载器：

-  **根类加载器**（bootstrap class loader）:它用来加载 Java 的核心类。
   - 是用原生代码来实现的，并不继承自 java.lang.ClassLoader, 即负责加载$JAVA_HOME中jre/lib/rt.jar里所有的class，由C++实现，不是ClassLoader子类

-  **扩展类加载器**（extensions class loader）：它负责加载JRE的扩展目录
   - lib/ext或者由java.ext.dirs系统属性指定的目录中的JAR包的类。由Java语言实现，父类加载器为null。
-  **系统类加载器**（system class loader）：被称为系统（也称为应用）类加载器。
   - 由Java语言实现，父类加载器为ExtClassLoader。
   - 它负责在JVM启动时加载来自Java命令的-classpath选项、java.class.path系统属性，或者CLASSPATH换将变量所指定的JAR包和类路径。
   - 程序可以通过ClassLoader的静态方法getSystemClassLoader()来获取系统类加载器。
   - 如果没有特别指定，则用户自定义的类加载器都以此类加载器作为父加载器



### 1.讲讲双亲委派机制

> 双亲委派模型不是一种强制性约束，也就是你不这么做也不会报错怎样的，它是一种JAVA设计者推荐使用类加载器的方式  

1.1 一句话原理：  
    双亲委派，其实是指Parent，即上级。双亲委派其实是【**丢给上级**】的意思 。  

当某个类加载器需要加载某个.class文件时，它首先把这个任务委托给他的上级类加载器，递归这个操作，如果上级的类加载器没有加载，自己才会去加载这个类。

1.2 类加载流程
![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6cfc8eeddbc94e39979d75cf513f933a~tplv-k3u1fbpfcp-watermark.image)


详细知识点可参考[知识点.3]

1.3 双亲委派的作用

- 1.防止重复加载同一个.class。通过委托去向上面问一问，加载过了，就不用再加载一遍。保证数据安全。
- 2.保证核心.class不能被篡改。通过委托方式，不会去篡改核心.clas，即使篡改也不会去加载，即使加载也不会是同一个.class对象了。不同的加载器加载同一个.class也不是同一个Class对象。这样保证了Class执行安全。
  

1.4 **破坏双亲委派目的往往是什么**  
人生不如意事十之八九，有些情况不得不违反这个约束，例如JDBC。  
你先得知道SPI(Service Provider Interface)，这玩意和API不一样，它是面向拓展的，也就是我定义了这个SPI，具体如何实现由扩展者实现。我就是定了个规矩。  

JDBC就是如此，在rt里面定义了这个SPI，那mysql有mysql的jdbc实现，oracle有oracle的jdbc实现，反正我java不管你内部如何实现的，反正你们都得统一按我这个来，这样我们java开发者才能容易的调用数据库操作。

所以**父加载器(根加载器)怎么可能知道你要加载什么呢？**   
肯定是你的业务代码才知道嘛
    
1.5 如何破坏双亲委派  
接上文的JDBC，
Java就搞了个线程上下文类加载器（Thread Context ClassLoader），
通过setContextClassLoader()默认情况就是应用程序类加载器然后Thread.current.currentThread().getContextClassLoader()获得类加载器来加载。



## 参考资料
1. [github-Guide哥的java知识集](https://github.com/Snailclimb/JavaGuide)
2. [jvm之java类加载机制和类加载器(ClassLoader)的详解](https://blog.csdn.net/m0_38075425/article/details/81627349)