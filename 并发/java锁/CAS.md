## CAS  

### 1. 一句话总结

- *compare and swap* 比较并交换；在更新值的时候检查下值有没有发生变化，如果没有发生变化则更新 
- 通过底层硬件获得原子性语句的支持。  
  哪条原子性语句呢？  
- cpu的 `lock cmpxchgl`  
  <br>

### 2. ABA问题

- 如果一个值原来是A，变成了B，又变成了A，那么使用CAS进行检查时会发现它的值没有发生变化，但是实际上却变化了。这就是CAS的ABA问题
- 解决思路：使用版本号
  - 在变量前面追加上版本号，每次变量更新的时候把版本号加一，那么A-B-A 就会变成1A-2B-3A。 目前在JDK的atomic包里提供了一个类AtomicStampedReference来解决ABA问题  

<br>

### 3. 是否要自旋 (比如 while(true){})

CAS的实现方式不同，

- 如果自旋就会导致本线程，本CPU不停的空转，浪费时间片；
  - 解决方案可以参照jdk8之后的 jdk#LongAdder设计
- 如果不自旋，就是超级乐观的锁设计，只适合线程冲突小的系统，因为不自旋的话，compare失败的线程就结束了(除非你再设计一套唤醒机制， 比如下面的AQS)

<br>

### 4.java的实现

java中使用Unsafe类调用c++代码

```java
public final boolean compareAndSet(int expect, int update) {   
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
}
```

这个本地方法在openjdk中依次调用的c++代码为：

- unsafe.cpp
- atomic.cpp
- atomicwindowsx86.inline.hpp
  最终走到下面的代码, *如果是多核cpu,就锁内存总线，保证原子性*

```c++
/ alternative for InterlockedCompareExchange
  int mp = os::is_MP();
  __asm {
    mov edx, dest
    mov ecx, exchange_value
    mov eax, compare_value
    LOCK_IF_MP(mp)
    cmpxchg dword ptr [edx], ecx
  }

```



