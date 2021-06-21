# log4j vs slf 4j

参考文章 (https://www.jianshu.com/p/7f787e3797a3)



## 一、log4j和slf4j的区别

log4j（ log for java ）（4 同 for）
Apache的一个开源项目，可以灵活地记录日志信息，我们可以通过Log4j的配置文件灵活配置日志的记录格式、记录级别、输出格式，而不需要修改已有的日志记录代码。
slf4j：simple log facade for java 简单日志门面
slf4j不是具体的日志解决方案，它只服务于各种各样的日志系统。按照官方的说法，SLF4J是一个用于日志系统的简单Facade，允许最终用户在部署其应用时使用其所希望的日志系统。
可以将log4j看成是一个完整的日志库，而slf4j是一个日志库的规范接口。



## 二、**那么使用slf4j有什么好处呢？**

#### 1. 让日志和项目之间解耦

想象一下这种场景，目前我们的项目已经使用了log4j作为日志库，有一天我们引入了一个技术大牛编写的组件，但是这个组件使用的是logback来进行日志输出，那么问题就来了，我们就不得不需要添加两个实现同样功能的jar包并且维护两套日子配置。
 而slf4j 是一个适配器，我们通过调用slf4j的日志方法统一打印我们的日志，而可以忽略其他日志的具体方法。

这样，**当我们的系统换了一个日志源后，不需要更改代码**



#### 2. 节省内存

log4j这些传统的日志系统里面并没有占位符的概念，当我们需要打印信息的时候，我们就不得不创建无用String对象来进行输出信息的拼接。



```cpp
    private void log4jTest(){
        String errormsg = "something error happen...";
        logger.info("错误信息为："+errormsg);
    }
```

**slf4j可以使用占位符，这样日志输出的时候就可以避免无用字符串对象的创建**



```cpp
    private void slf4jTest(){
    logger.info("错误信息为：{}","something error happen...");
    }
```

