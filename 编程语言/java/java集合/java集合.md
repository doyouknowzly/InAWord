# 简单分类:

| 线程安全性   | 大类 | 集合                 | 一句话知识点                                                 |
| ------------ | ---- | -------------------- | ------------------------------------------------------------ |
| 线程不安全的 | List | ArrayList            | ArrayList底层的数据结构是数组，数组元素类型是Object，即内部是用Object[]实现的 |
|              |      | LinkedList           | LinkedList 底层使⽤的是 双向链表 数据结构（JDK1.6 之前为循环链表，JDK1.7 取消了循环。) |
|              | Set  | HahSet               | 使用HashMap来实现, <br>value是一个内部的静态Object, 只是占位而已。本质就是用一下HashMap的key |
|              |      | TreeSet              | 和HashSet类似，本质通过new了一个TreeMap实现功能， 使用了它的KeySet，value用了内部的静态Object对象 |
|              |      | LinkedHashSet        |                                                              |
|              | Map  | HashMap              | JDK1.7以前: 数组 + 链表 <br>JDK1.8以后: 数组 + 红黑树        |
|              |      |                      |                                                              |
| 线程安全的   | List | Vector               | 给几乎所有的public方法都加上了synchronized关键字             |
|              |      | CopyOnWriteArrayList |                                                              |
|              | Set  | CopyOnWriteArraySet  |                                                              |
|              | Map  | HashTable            | 它给几乎所有public方法都加上了synchronized关键字，因此性能欠佳<br>**HashTable的K，V都不能为null** |
|              |      | ConcurrentHashMap    |                                                              |

> Tips：多线程的K-V集合基本都不允许value为null, 因为如果允许就会存在二义性：null是有这个value, 还是没get到返回null ； 
> 单线程的集合允许为null， 因为当前线程自己知道自己的逻辑，到底是没get到还是存了null。

# 一句话知识点:

## A.各种集合类的初始化容量、扩容时机

| 集合类              | 初始容量 | 扩容时机                                          | 扩容策略                                                    |
| ------------------- | -------- | ------------------------------------------------- | ----------------------------------------------------------- |
| ArrayList           | 10       | add()的时候触发ensureCapacity()，满了就扩容       | 扩容为1.5倍， 再把老数组的元素存储到新数组里面              |
| HashMap             | 16       | 容量= size * 负载因子的时候，初始是16 * 0.75 = 12 | 扩容为2倍， 将数据rehash， 然后复制过去(扩容时非常影响性能) |
| HashTable           | 11       |                                                   | 扩容为2倍 + 1                                               |
| LinkedList、TreeSet |          | 基于链表，不需要扩容                              |                                                             |
| HashSet             |          |                                                   |                                                             |





## C.ConcurrentHashMap

| 序号 | 问题                                            |
| ---- | ----------------------------------------------- |
| 1    | ConcurrentHashMap在JDK1.7和1.8的实现区别        |
| 2    | 1.8中为什么放弃了分段锁Segment                  |
| 3    | ConcurrentHashMap在扩容的时候，怎么保证线程安全 |

## 详细解答

### C1、ConcurrentHashMap在JDK1.7和1.8的实现区别

分段锁的思路是: **降低冲突概率**

一个锁变成多个锁，如果多个线程在请求不同的hash段，是可以并发进行不竞争锁的。

### C2、1.8中为什么放弃了分段锁Segment

### C3、ConcurrentHashMap在扩容时怎么保证线程安全？

**等扩容完之后，所有的读写操作才能进行**，所以扩容的效率就成为了整个并发的一个瓶颈点。  
好在Doug lea教授对扩容做了优化，本来在一个线程扩容的时候，如果影响了其他线程的数据，那么其他的线程的读写操作都应该阻塞。  
但Doug lea说你们闲着也是闲着，不如来一起参与扩容任务，这样人多力量大，办完事你们该干啥干啥，别浪费时间，于是在JDK8的源码里面就引入了一个ForwardingNode类来实现多线程协作扩容.

参考文章[<<理解Java7和8里面HashMap+ConcurrentHashMap的扩容策略>>](https://blog.csdn.net/u010454030/article/details/82458413)