## GC参数

https://www.oracle.com/java/technologies/javase/javase-core-technologies-apis.html

[oracle官方<<JVM内存管理文档>>](https://www.oracle.com/technetwork/java/javase/tech/memorymanagement-whitepaper-1-150020.pdf)



从Hotspot参考文档来看jdk11已经将GC部分的参数按照收集器类型进行了分类，分为：

- G1收集器参数
- CMS收集器参数
- Parallel收集器参数
- 通用参数



JVM调优，参考文档

(https://github.com/qiurunze123/memoryoptimization/blob/master/docs/jvmggggo.md)

(https://github.com/qiurunze123/memoryoptimization)



### 通用参数

| 分类                   | 参数                        | 解释                                                         | 默认值                 |
| ---------------------- | --------------------------- | ------------------------------------------------------------ | ---------------------- |
| 打印GC日志             | PrintGC                     | 垃圾收集时打印message                                        | false                  |
|                        | PrintGCDetails              | 打印GC详细日志                                               | false                  |
|                        | PrintGCCause                | 在GC日志中打印GC原因                                         | true                   |
|                        | PrintGCDateStamps           | 打印GC日期信息                                               | false                  |
|                        | PrintGCTimeStamps           | 打印GC时间戳信息                                             | false                  |
|                        | PrintGCID                   | 打印每次GC的ID                                               | false                  |
|                        | PrintGCTaskTimeStamps       | 打印单个gc工作线程任务的时间戳                               | false                  |
|                        | PrintReferenceGC            | 打印GC期间花在处理对象引用关系上的时间（仅在开启了PrintGCDetails才有用） | false                  |
|                        | HeapDumpBeforeFullGC        | 在Full GC前生成heap dump文件                                 | false                  |
|                        | HeapDumpAfterFullGC         | 在Full GC后生成heap dump文件                                 | false                  |
|                        |                             |                                                              |                        |
|                        |                             |                                                              |                        |
| 声明使用哪种垃圾收集器 | UseSerialGC                 |                                                              | false                  |
|                        | UseConcMarkSweepGC          | 开启后会**自动开启UseParNewGC**                              | false                  |
|                        | UseG1GC                     |                                                              | false                  |
|                        | UseParallelGC               |                                                              | true                   |
|                        | UseParallelOldGC            |                                                              | false                  |
|                        | UseParNewGC                 |                                                              | false                  |
|                        |                             |                                                              |                        |
| 控制gc线程             | ParallelGCThreads           | 控制多线程垃圾收集器收集线程的**并行数** <br>如果Java API Runtime.availableProcessors()<=8，则此参数默认为ParallelGCThreads值，<br>否则为8+（Runtime.availableProcessors()­8)*5/8 | 0                      |
|                        | UseDynamicNumberOfGCThreads | 动态选择gc使用线程数                                         | false                  |
|                        | HeapSizePerGCThread         | 根据堆大小计算,每个线程负责多大空间<br>active_works=max(2, heap.capacity() / HeapSizePerGCThread) | ScaleForWordSize(64*M) |
|                        | ConcGCThreads               | 选择gc并发线程数                                             | 0                      |
|                        | GCTaskTimeStampEntries      | Parallel收集器参数，每个gc工作线程的时间戳条数               | 200                    |
|                        |                             |                                                              |                        |
|                        |                             |                                                              |                        |
|                        |                             |                                                              |                        |
|                        |                             |                                                              |                        |
| GC策略                 | ScavengeBeforeFullGC        | parallel收集器参数，在执行full GC前先执行一次youong GC，以缩短full GC最大停顿时间，<br/>默认开启 | true                   |
|                        |                             |                                                              |                        |





### 收集器相关的参数

##### CMS参数

| 分类 | 参数                        | 解释                                                         | 默认值 |
| ---- | --------------------------- | ------------------------------------------------------------ | ------ |
|      | ExplicitGCInvokesConcurrent | 打开此参数后，在调用System.gc()时会做background模式CMS GC，可提高FULL GC效率<br/>（仅在XX:+UseConcMarkSweepGC时有效） | false  |
|      |                             |                                                              |        |
|      |                             |                                                              |        |
|      |                             |                                                              |        |



##### G1参数

| 分类 | 参数                           | 解释                                                         | 默认值      |
| ---- | ------------------------------ | ------------------------------------------------------------ | ----------- |
|      | MaxGCPauseMills                | 期望的GC停顿时间，G1会动态改变堆空间的配比，GC的策略来满足期待时间 | 200，单位ms |
|      | InitiatingHeapOccupancyPercent | 触发并发GC周期时的堆内存占用百分比. G1之类的垃圾收集器用它来触发并发GC周期,<br/>基于整个堆的使用率,而不只是某一代内存的使用比. 值为 0 则表示”一直执行GC循环 | 45          |
|      |                                |                                                              |             |
|      |                                |                                                              |             |
|      |                                |                                                              |             |
|      |                                |                                                              |             |
|      |                                |                                                              |             |

