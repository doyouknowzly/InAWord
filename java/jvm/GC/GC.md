## 面试题

| 序号 | 问题                                  | 一句话总结                                                   |
| ---- | ------------------------------------- | ------------------------------------------------------------ |
| 0    | 如何判断对象已经死亡，即需要GC？      | 可达性分析vs引用计数法                                       |
| 1    | GC算法有哪些                          | 标记-清除<br>标记-整理<br>复制                               |
| 2    | 垃圾回收器都有哪些，可以怎么配合      |                                                              |
| 3    | 有哪几种GC，触发条件分别是什么        | 新生代GC (Minor GC)<br>老年代GC (Major GC)<br/>全局GC (Full GC) |
| 4    | GC失败的情况有哪些，怎么处理          |                                                              |
| 5    | 一次完整的GC流程                      |                                                              |
| 6    | GC相关的jvm参数都有哪些，可以如何调优 | 详见<<GC参数>>                                               |
| 7    | 内存分配与回收策略                    |                                                              |
| 8    | CMS细节                               |                                                              |
| 9    | G1细节                                |                                                              |
| 10   | Z收集器细节                           |                                                              |

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

   

2. 引用计数法

   所谓的引用计数法就是给每个对象一个引用计数器，每当有一个地方引用它时，计数器就会加1；当引用失效时，计数器的值就会减1；

   任何时刻计数器的值为0的对象就是不可能再被使用的。

   >  这个引用计数法时没有被Java所使用的，但是python有使用到它。而且最原始的引用计数法没有用到GC Roots。

### 1. GC算法有哪些

1. 常见的GC算法有哪些，各自的特点是什么
   一般是3种：【标记-清除】and 【复制】and 【标记-整理】  

- 标记- 清除算法

  - 该算法分为“标记”和“清除”阶段：⾸先标记出所有不需要回收的对象，在标记完成后统⼀回收掉所有没有被标记的对象。
  - 它是最基础的收集算法，后续的算法都是对其不⾜进⾏改进得到。
  - 这种垃圾收集算法会带来两个明显的问题：
    - 1. 效率问题
    - 2. 空间问题(标记清除后会产⽣⼤量不连续的碎⽚)  

  ![image.png](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f73566a5f32f48b58a3d022420997f9c~tplv-k3u1fbpfcp-watermark.image)

- 复制算法

  - 为了解决效率问题，“复制”收集算法出现了。
  - 它可以将内存分为⼤⼩相同的两块，每次使⽤其中的⼀块。当这⼀块的内存使⽤完后，就将还存活的对象复制到另⼀块去，然后再把使⽤的空间⼀次清理掉。这样就使每次的内存回收都是对内存区间的⼀半进⾏回收。
  - 优点： 高效、没有内存碎片 (正好是标记-清除 算法的缺点)
  - 缺点： 浪费空间，至少有一半的空间被浪费

  

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/40ccd6a990a243178ef3cc36eca22aed~tplv-k3u1fbpfcp-watermark.image)
      

- 标记- 整理算法
  - 标记过程仍然与“标记-清除”算法⼀样，但后续步骤不是直接对可回收对象回收，⽽是让所有存活的对象向⼀端移动，然后直接清理掉端边界以外的内存。
  - 一般是根据⽼年代的特点提出的⼀种标记算法，

- 分代收集。其实不是一种算法，而只是一种思路：  
  - 只是根据对象存活周期的不同将内存分为⼏块。⼀般将 java 堆分为新⽣代和⽼年代，这样我们就可以根据各个年代的特点选择合适的垃圾收集算法。  

  - 目的： 分类，然后提高GC效率  

  - 使用思路：
    - ⽐如在新⽣代中，每次收集都会有⼤量对象死去，所以可以选择复制算法，高效  
    - ⽽⽼年代的对象存活⼏率是⽐较⾼的，⽽且没有额外的空间对它进⾏分配担保，所以我们必须选择“标记-清除”或“标记-整理”算法进⾏垃圾收集
    
    

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



### 7.内存分配与回收策略

1. **对象优先在Eden区分配**

   当Eden区没有足够空间进行分配时，虚拟机将发起一次Minor GC

2. **大对象直接进入老年代**

   - 因为大对象如果进入Eden区可能会导致正常的小对象没多少空间, 频繁GC
   - 大对象GC的时候还要复制，很麻烦的
   - -XX:PretenureSizeThreshold参数，令大于这个设置值的对象直接在老年代分配 【**只对Serial和ParNew两款收集器有效**】

3. **长期存活的对象将进入老年代**

   - 具体策略:
     - 如果对象在Eden出生并经过第一次Minor GC后仍然存活，并且能被Survivor容纳的话，将被移动到Survivor空间中，并且对象年龄设为1。
     - 对象在Survivor区中每“熬过”一次Minor GC，年龄就增加1岁。
     - 当它的年龄增加到一定程度（默认为15岁），就将会被晋升到老年代。

   	> 对象晋升老年代的年龄阈值，可以通过参数-XX:MaxTenuringThreshold设置

4. **动态年龄判定**

   为了能更好地适应不同程序的内存状况，虚拟机并不是永远地要求对象的年龄必须达到了MaxTenuringThreshold才能晋升老年代。

   如果在Survivor空间中相同年龄(比如6岁)所有对象大小的总和大于Survivor空间的一半，年龄大于或等于该年龄的对象就可以直接进入老年代，无须等到MaxTenuringThreshold中要求的年龄。

5. **空间分配担保**

   思路: 

   ​	通过一些比较，看看只进行MinorGC, 能不能释放出足够的空间； 因为MinorGC后，很可能触发晋升，所以要老年代担保有足够的空间晋升

   具体流程: 

   ​	在发生Minor GC之前，虚拟机会先检查老年代最大可用的连续空间是否大于新生代所有对象总空间

   - 如果这个条件成立，那么Minor GC可以确保是安全的
   - 如果不成立，则虚拟机会查看HandlePromotionFailure设置值是否允许担保失败（**JDK6以后此参数无效**）
     - 如果不允许，进行一次FULL GC
     - 如果允许， 那么会继续检查老年代最大可用的连续空间是否大于历次晋升到老年代对象的平均大小
       - 如果大于， 将尝试着进行一次Minor GC，尽管这次Minor GC是有风险的
       - 如果小于， 进行一次FULL GC
   - 如果某次Minor GC存活后的对象突增，远远高于平均值的话，依然会导致担保失败（Handle Promotion Failure）
     - 如果出现了HandlePromotionFailure失败，那就只好在失败后重新发起一次FullGC
   - 虽然担保失败时绕的圈子是最大的，但大部分情况下都还是会将HandlePromotionFailure开关打开，避免Full GC过于频繁

   **JDK6之后的新流程** : 

   ​	只要老年代的连续空间大于**新生代对象总大小**或者**历次晋升的平均大小**就会进行Minor GC，否则将进行Full GC。

   