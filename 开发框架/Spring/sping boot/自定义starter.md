## 自定义starter：

| 序号 | 问题                    | 一句话概述                                                   |
| ---- | ----------------------- | ------------------------------------------------------------ |
| 0    | 自定义starter的作用     | 抛弃以前繁杂的配置， 只需要在maven中引入starter依赖，IOC容器就能自动装填目标Bean |
| 1    | 自定义starter的使用思路 | 自动通过classpath路径下的类发现需要的Bean，及配置Bean的类， 利用他们生成Bean并装填 |
| 2    | 如何编写                |                                                              |
| 3    | 最佳实践                |                                                              |
| 4    | demo示例                |                                                              |



### 1、如何编写自动配置

```java
@Configuration  //指定这个类是一个配置类
@ConditionalOnXXX  //在指定条件成立的情况下自动配置类生效
@AutoConfigureAfter  //指定自动配置类的顺序
@Bean  //给容器中添加组件

@ConfigurationPropertie结合相关xxxProperties类来绑定相关的配置
@EnableConfigurationProperties //让xxxProperties生效加入到容器中

自动配置类要能加载
将需要启动就加载的自动配置类，配置在META-INF/spring.factories
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.springframework.boot.autoconfigure.admin.SpringApplicationAdminJmxAutoConfiguration,\
org.springframework.boot.autoconfigure.aop.AopAutoConfiguration,\

```

### 2、最佳实践：

- starter模块只用来做依赖导入；

- 专门来写一个自动配置模块, 核心代码写在这里；

- starter依赖自动配置；别人只需要引入starter



大部分开源项目都是上面👆这种思路，例如

mybatis-spring-boot-starter；自定义启动器名-spring-boot-starter



### 3、demo示例



```java
package com.zly.starter;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "com.zly.hello")
public class HelloProperties {

    private String prefix;
    private String suffix;

    public String getPrefix() {
        return prefix;
    }

    public void setPrefix(String prefix) {
        this.prefix = prefix;
    }

    public String getSuffix() {
        return suffix;
    }

    public void setSuffix(String suffix) {
        this.suffix = suffix;
    }
}


```



```java
package com.zly.starter;

public class HelloService {

    HelloProperties helloProperties;

    public HelloProperties getHelloProperties() {
        return helloProperties;
    }

    public void setHelloProperties(HelloProperties helloProperties) {
        this.helloProperties = helloProperties;
    }

    public String sayHellAtguigu(String name){
        return helloProperties.getPrefix()+"-" 
            +name + helloProperties.getSuffix();
    }
}


```





```java
package com.zly.starter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnWebApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(HelloProperties.class)
public class HelloServiceAutoConfiguration {

    @Autowired
    HelloProperties helloProperties;
    @Bean
    public HelloService helloService(){
        HelloService service = new HelloService();
        service.setHelloProperties(helloProperties);
        return service;
    }
}


```

