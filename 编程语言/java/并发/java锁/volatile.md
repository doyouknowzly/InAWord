## volatile

### 1.简介

轻量级地解决线程同步问题  

### 2.作用

- 【保证线程可见性】
- 【禁止指令重排序】
- 【不保证原子性】


### 3.原理

- 一句话原理
  voaltile关键字  --> jvm 字节码【ACC_VOLATILE】 --> 
  c++【voaltile关键字 】--> 【lock addl】 实现

- 实现可见性
  通过Lock前缀实现可见性，lock指令下一条指令，
  写完缓存后，当前CPU回写主存，
  并立即通知其他线程重新读缓存行
- 实现有序性

> JMM层面的“内存屏障”：
> LoadLoad屏障： 对于这样的语句Load1; LoadLoad; Load2，在Load2及后续读取操作要读取的数据被访问前，保证Load1要读取的数据被读取完毕。
> StoreStore屏障：对于这样的语句Store1; StoreStore; Store2，在Store2及后续写入操作执行前，保证Store1的写入操作对其它处理器可见。
> LoadStore屏障：对于这样的语句Load1; LoadStore; Store2，在Store2及后续写入操作被刷出前，保证Load1要读取的数据被读取完毕。
> StoreLoad屏障： 对于这样的语句Store1; StoreLoad; Load2，在Load2及后续所有读取操作执行前，保证Store1的写入对所有处理器可见。

- JVM的实现会在volatile读写前后均加上内存屏障，在一定程度上保证有序性。如下所示：

```java 
LoadLoadBarrier  
volatile 读操作  
LoadStoreBarrier 

StoreStoreBarrier  
volatile 写操作  
StoreLoadBarrier  
```

但上面的内存屏障只是jvm的实现要求， Hot spot实现还是汇编的lock addl指令实现的

addl把寄存器的值加0，相当于一个空操作,关键还是想要addl前面的[lock]
（之所以用addl，不用空操作专用指令nop，是因为lock前缀不允许配合nop指令使用）