使用注解和AOP , catch住异常，然后返回状态码

1. 自定义注解

```java
package com.zly.usingspringboot.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Target(ElementType.METHOD)
@Retention(RUNTIME)
public @interface ExceptionCatch {
}

```

2. AOP处理类

```java
package com.zly.usingspringboot.annotation;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
@Aspect
public class ExceptionCatchHandler {

    private Logger logger1 = LoggerFactory.getLogger(this.getClass());

    @Pointcut("@annotation(com.zly.usingspringboot.annotation.ExceptionCatch)")
    public void pointCutException(){

    }

    @Around("pointCutException()")
    public Object handleException(ProceedingJoinPoint joinPoint){
        try{
            logger1.info("before around run");
            return joinPoint.proceed();
        }catch (Throwable e){
            Logger logger = LoggerFactory.getLogger(joinPoint.getTarget().getClass());
            String className = joinPoint.getTarget().getClass().getName();
            String methodName = joinPoint.getSignature().getName();
            Object[] args = joinPoint.getArgs();

            StringBuilder params = new StringBuilder();
            for (Object arg : args) {
                params.append(arg).append(" ");
            }

            logger.warn("zly catch you! ");
            logger.warn("while call the method:{}, of the class:{}, params are:{}",
                    methodName, className, params.toString());
        }

        return "catch";
    }
}

```

