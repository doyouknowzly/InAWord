## Atomic类



### 1. 一句话总结

- atomic类是通过自旋+CAS操作+volatile变量实现的。
  ![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d0e962ca948d4c2285f77bd0e16203a8~tplv-k3u1fbpfcp-watermark.image)

### 2. jdk8 的LongAdder 和 AtomicLong相比，优化了哪里？

高并发下N多线程同时去操作一个变量会造成大量线程CAS失败，然后处于自旋状态，导致严重浪费CPU资源，降低了并发性。既然AtomicLong性能问题是由于过多线程同时去竞争同一个变量的更新而降低的，那么如果把一个变量分解为多个变量，让同样多的线程去竞争多个资源，这就是LongAdder的原理。  
![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5074a82ac3014db2a0233a383ad6f8ca~tplv-k3u1fbpfcp-watermark.image)  
LongAdder则是内部维护一个Cells数组，每个Cell里面有一个初始值为0的long型变量，在同等并发量的情况下，争夺单个变量的线程会减少，这是变相的减少了争夺共享资源的并发量，另外多个线程在争夺同一个原子变量时候，如果失败并不是自旋CAS重试，而是尝试获取其他原子变量的锁，最后当获取当前值时候是把所有变量的值累加后再加上base的值返回的。

