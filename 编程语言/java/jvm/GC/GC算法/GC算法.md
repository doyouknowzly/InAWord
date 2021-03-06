# GC算法

当前商业虚拟机的垃圾收集器，大多数都遵循了“分代收集”（Generational Collection）的理论进 行设计。

分代收集名为理论，实质是一套符合大多数程序运行实际情况的经验法则，它建立在两个分 代假说之上： 

1）**弱分代假说（Weak Generational Hypothesis）**：绝大多数对象都是朝生夕灭的。 

2）**强分代假说（Strong Generational Hypothesis）**：熬过越多次垃圾收集过程的对象就越难以消 亡。



但这样存在一个明显的困难：对象不 是孤立的，对象之间会存在跨代引用。

假如要现在进行一次只局限于新生代区域内的收集（Minor GC），但新生代中的对象是完全有可 能被老年代所引用的，

为了找出该区域中的存活对象，不得不在固定的GC Roots之外，再额外遍历整 个老年代中所有对象来确保可达性分析结果的正确性，反过来也是一样



为了解决这个问题，就需要对分 代收集理论添加第三条经验法则：

3）**跨代引用假说（Intergenerational Reference Hypothesis）**：跨代引用相对于同代引用来说仅占极少数。

这其实是可根据前两条假说逻辑推理得出的隐含推论：存在互相引用关系的两个对象，是应该倾 向于同时生存或者同时消亡的。

> 举个例子，如果某个新生代对象存在跨代引用，由于老年代对象难以 消亡，该引用会使得新生代对象在收集时同样得以存活，进而在年龄增长之后晋升到老年代中，这时 跨代引用也随即被消除了。



## 一、 标记- 清除算法

最早出现的GC算法

- 该算法分为“标记”和“清除”阶段：首先标记出所有不需要回收的对象，在标记完成后统⼀回收掉所有没有被标记的对象。

- 它是最基础的收集算法，后续的算法都是对其不⾜进⾏改进得到。

  <img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/f73566a5f32f48b58a3d022420997f9c~tplv-k3u1fbpfcp-watermark.image" alt="image.png" style="zoom:67%;" />

这种垃圾收集算法会带来两个明显的问题：

1. 效率问题，如果有大量对象要回收，则标记、清理阶段的耗时都会线性增长
2. 空间问题(标记清除后会产⽣⼤量不连续的碎片)

     

## 二、复制算法

为了解决标记-清除的效率问题，“复制”收集算法出现了。

它可以将内存分为大小相同的两块，每次使⽤其中的⼀块。

当这⼀块的内存使⽤完后，就将还存活的对象复制到另⼀块去，然后再把使⽤的空间⼀次清理掉。这样就使每次的内存回收都是对内存区间的⼀半进⾏回收。

<img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/40ccd6a990a243178ef3cc36eca22aed~tplv-k3u1fbpfcp-watermark.image" alt="image.png" style="zoom:67%;" />

- 优点： 高效、没有内存碎片 (正好是标记-清除 算法的缺点)
- 缺点： 浪费空间，至少有一半的空间被浪费



​	现在的商用Java虚拟机大多都优先采用了这种收集算法去回收新生代，IBM公司曾有一项专门研 究对新生代“朝生夕灭”的特点做了更量化的诠释——新生代中的对象有98%熬不过第一轮收集。 因此 并不需要按照1∶1的比例来划分新生代的内存空间。

​	具体做法是把新生代分为一块较大的Eden空间和两块较小的 Survivor空间，每次分配内存只使用Eden和其中一块Survivor。

发生垃圾收集时，将Eden和Survivor中仍 然存活的对象一次性复制到另外一块Survivor空间上，然后直接清理掉Eden和已用过的那块Survivor空 间。

HotSpot虚拟机默认Eden和Survivor的大小比例是8∶1，也即每次新生代中可用内存空间为整个新 生代容量的90%（Eden的80%加上一个Survivor所占的10%）

> 10%的新生代是会 被“浪费”的 (即其中的一块Survivor区)



## 三、标记-整理算法

> 复制算法在对象存活率较高时就要进行较多的复制操作，效率将会降低。更关键的是，如果 不想浪费50%的空间，就需要有额外的空间进行分配担保，以应对被使用的内存中所有对象都100%存 活的极端情况，所以在老年代一般不能直接选用复制算法。

标记-整理算法，标记过程仍然与“标记-清除”算法⼀样，但后续步骤不是直接对可回收对象回收，⽽是让所有存活的对象向⼀端移动，然后直接清理掉端边界以外的内存。

移动时，将会且必须STW，这会导致延时增高，但因为能避免碎片化问题，总的吞吐量还是比标记-清除算法高的。

一般是根据⽼年代的特点提出的⼀种标记算法.

