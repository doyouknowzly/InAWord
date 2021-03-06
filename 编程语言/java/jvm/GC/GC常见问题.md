

# GC常见问题



GC有三大核心问题:   what, when ,how，即

- 哪些内存需要回收？
- 何时回收？
- 如何回收？



下面的问题列表，其实都是基于上面的3个核心问题引申的



| 序号 | 问题                                  | 一句话总结                                                   |
| ---- | ------------------------------------- | ------------------------------------------------------------ |
| 0    | 如何判断对象已经死亡，即需要GC？      | 可达性分析vs引用计数法                                       |
| 1    | GC算法有哪些                          | 标记-清除<br>标记-整理<br>复制<br>参考: [GC算法](./GC算法)   |
| 2    | 垃圾回收器都有哪些，可以怎么配合      | 参考 [垃圾收集器](./垃圾收集器/垃圾收集器)                   |
| 3    | 有哪几种GC，触发条件分别是什么        | 新生代GC (Minor GC)<br>老年代GC (Major GC)<br/>全局GC (Full GC) |
| 4    | GC失败的情况有哪些，怎么处理          |                                                              |
| 5    | 一次完整的GC流程                      |                                                              |
| 6    | GC相关的jvm参数都有哪些，可以如何调优 | 详见<<GC参数>>                                               |
| 7    | 内存分配与回收策略                    |                                                              |
| 8    | 什么是浮动垃圾, 怎么处理              |                                                              |
|      |                                       |                                                              |



### 0. 如何判断对象已经死亡，需要GC？

1. 可达性分析

   当一个对象不可达时，就认为该对象用不到了，可以GC了。

   所谓的可达性就是通过一系列称为“GC Roots”的对象为起点从这些节点开始向下搜索，搜索走过的路径称为引用链，当一个对象到GC Roots没有任何引用链相连（用图论的话来说，就是GC Roots到这个对象不可达）时，则说明此对象是不可用的。

   

   那么那些对象可以作为GC Roots呢？以Java为例，有以下几种：

   - 栈（栈帧中的本地变量表）中引用的对象。

   - 方法区中的静态成员。

   - 方法区中的常量引用的对象（全局变量）。

   - 本地方法栈中JNI（一般说的Native方法）引用的对象。

   注：第一和第四种都是指的方法的本地变量表，第二种表达的意思比较清晰，第三种主要指的是声明为final的常量值。

   > 至于什么是引用，参考 [引用](../强软弱虚reference)



​		注2: 实际上，标记一个对象已死的时候，并不需要每次都从GC Roots完整地遍历一遍。

​		在HotSpot 的解决方案里，是使用一组称为**OopMap**的数据结构来达到这个目的。

​		一旦类加载动作完成的时候， HotSpot就会把对象内什么偏移量上是什么类型的数据计算出来，也 会在特定的位置记录下栈里和寄存器里哪些位置是引用。



2. 引用计数法

   所谓的引用计数法就是给每个对象一个引用计数器，每当有一个地方引用它时，计数器就会加1；当引用失效时，计数器的值就会减1；

   任何时刻计数器的值为0的对象就是不可能再被使用的。

   > 这个引用计数法没有被Java所使用，但是python有使用到它。而且最原始的引用计数法没有用到GC Roots。

  缺点: 如果有a,b循环引用，外部其实用不到他们了，但是引用计数法还是认为a,b未死

- - -



**注意：** 当一个对象A 已经没有GC Roots可达时，也不是就立即被标记为"死亡"的。

如果A对应的类实现了finalize()方法， 并且对于A对象，还从未执行过finalize()方法， jvm就会将A放到F-QUEUE队列中，有一个线程会逐个调用对象们的这个方法，可能会实现对象的"自救"，即找到任一GC Roots引用自己

> 但 <<深入理解Java虚拟机>>作者不鼓励使用这个方法，因为很少有人这么用， finally语句也能完成类似的作用，且更好理解



### 3. 有哪几种GC，触发条件分别是什么

- 新生代GC（Minor GC/ Young GC）：指发生在新生代的垃圾收集动作.

  因为Java对象大多都具备朝生夕灭的特性，所以Minor GC非常频繁，一般回收速度也比较快。

  - 触发条件: 当Eden区没有足够空间进行分配时，虚拟机将发起一次Minor GC

- 老年代GC（Major GC / Old GC）：指发生在老年代的GC.

  出现了Major GC，经常会伴随至少一次的Minor GC（但非绝对的，在Parallel Scavenge收集器的收集策略里就有直接进行Major GC的策略选择过程）.
  
  - Major GC的速度一般会比Minor GC慢10倍以上。
  
- Mixed GC: 收集整个young gen 以及部分old gen的GC。

  **只有垃圾收集器 G1有这个模式**

- Full GC: 收集整个堆，包括 新生代，老年代，永久代(在 JDK 1.8及以后，永久代被移除，换为metaspace 元空间)等所有部分的模式

  另外，如果分配了Direct Memory，在老年代中进行Full GC时，会顺便清理掉Direct Memory中的废弃对象。

  - 针对不同的垃圾收集器，**Full GC的触发条件可能不都一样**
  - 一般情况下有这些条件: 
    - 担保失败
    - 永久代or元空间没有足够的内存
    - 手动System.gc()

### 4. GC失败的情况有哪些，怎么处理



### 5. 一次完整的GC流程

