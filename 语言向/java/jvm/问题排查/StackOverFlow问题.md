# StackOverflow问题



#### **每一个 JVM 线程都拥有一个私有的 JVM 线程栈，用于存放当前线程的 JVM 栈帧(包括被调用函数的参数、局部变量和返回地址等)。如果某个线程的线程栈空间被耗尽，没有足够资源分配给新创建的栈帧，就会抛出 \**java.lang.StackOverflowError\** \**错误。\****



当 main()  方法被调用后，执行线程按照代码执行顺序，将它正在执行的方法、基本数据类型、对象指针和返回值包装在栈帧中，逐一压入其私有的调用栈，整体执行过程如下图所示：

![0b85ed8a9dc0fa3b382b0375330d7060.png](https://img-blog.csdnimg.cn/img_convert/0b85ed8a9dc0fa3b382b0375330d7060.png)

如上所述，JVM 线程栈存储了方法的执行过程、基本数据类型、局部变量、对象指针和返回值等信息，这些都需要消耗内存。 一旦线程栈的大小增长超过了允许的内存限制，就会抛出 java.lang.StackOverflowError 错误。 下面这段代码通过无限递归调用最终引发了 java.lang.StackOverflowError 错误。

```java
public class StackOverflowErrorExample {public static void main(String args[]) {
            a();
      }public static void a() {
            a();
      }
}
```

在这种情况下，a() 方法将无限入栈，直至栈溢出，耗尽线程栈空间，如下图所示。

![f88ba728bdf3272d17af1b4b073c9409.png](https://img-blog.csdnimg.cn/img_convert/f88ba728bdf3272d17af1b4b073c9409.png)


### 默认栈空间大小

线程栈的默认大小依赖于操作系统、JVM 版本和供应商，常见的默认配置如下表所示：

| JVM 版本                     | 线程栈默认大小<br/> |
| ---------------------------- | ------------------- |
| Sparc 32-bit JVM             | 512 kb<br/>         |
| Sparc 64-bit JVM             | 1024 kb<br/>        |
| x86 Solaris/Linux 32-bit JVM | 320 kb<br/>         |
| x86 Solaris/Linux 64-bit JVM | 1024 kb<br/>        |
| Windows 32-bit JVM           | 320 kb<br/>         |
| Windows 64-bit JVM           | 1024 kb             |






### 常见原因: 

1. 无限循环、死循环
2. 局部变量过多、过大
3. 使用了 gson 序列化， 而gson处理不了对象循环引用的问题



### 解决方案: 

1. 优化代码，处理不恰当的循环
2. 通过 -Xss1024K  这样的配置，提升栈空间大小
3. 复杂对象，不使用gson, 换FastJson等 