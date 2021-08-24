# HashMap

参考文档

https://www.zhihu.com/question/20733617/answer/2022919698

| 序号 | 问题                                                         | 一句话知识点                                                 |      |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| 1    | HashMap的扩容怎么发生的，有哪些注意的                        |                                                              |      |
| 2    | HashMap的实现原理，JDK1.7和1.8                               | JDK1.7以前: 数组 + 链表 <br/>JDK1.8以后: 数组 + 红黑树       |      |
| 3    | HashMap的容量为什么总是2的幂？手动指定容量 会不会破坏这个设计？ | 求余计算可以简化成位运算&<br>不会，会对齐                    |      |
| 4    | put()方法的流程                                              |                                                              |      |
| 5    | 负载因子是什么？为什么是0.75                                 | 遵循泊松分布，在0.75的时候，空间和时间的取舍是比较巧妙的     |      |
| 6    | HashMap怎么解决Hash冲突的                                    | 先尝试扰动函数进行扰动;<br>如果扰动后还是冲突，就使用"链式寻址法";<br>实在冲突太多，就转换成红黑树咯 |      |
| 7    | HashMap的死循环                                              |                                                              |      |
| 8    | 为什么要在1.8引入红黑树                                      | 如果hash方法设计得好，hash冲突少，最长的槽length <8, 其实链表是不会转换成红黑树的; <br>所以红黑树就是用来优化那些随机程度不够的，自定义的hash算法的性能的 |      |
| 9    | HashMap中的元素为什么要同时覆写equals()和hashCode()          | 重点是put()和get()的流程<br>先hashCode(),  再equals()<br>要区分key和value分别是自定义类的对象A的时候，分别讨论 |      |
| 10   | HashMap的 hash()函数原理                                     | 扰动函数                                                     |      |
| 11   | Object的默认hashCode代码原理                                 |                                                              |      |

## 详细解答

### 2、HashMap的实现原理，JDK1.7和1.8？

- 对比
  ![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/789518752776473d930beed2f5ef56fa~tplv-k3u1fbpfcp-watermark.image)

  参考(https://zhuanlan.zhihu.com/p/69035659)



### 3、HashMap的容量为什么总是2的幂？手动指定容量 会不会破坏这个设计？

Hash 值的范围值 2^32 (-2147483648到2147483647)，前后加起来⼤概40亿的映射空间，只要
哈希函数映射得⽐᫾均匀松散，⼀般应⽤是很难出现碰撞的。但问题是⼀个40亿⻓度的数组，内
存是放不下的。所以这个散列值是不能直接拿来⽤的。⽤之前还要先做对数组的⻓度取模运算，即hash % length
而重点是，如果满足下面的条件：

- length 是2的幂
  就可以有这样的等式hash%length==hash&(length-1) (数学证明略)  
   即**这种情况下，求余计算可以简化成位运算&**, 位运算大家都知道吧？CPU一个时钟周期就完成啦！

<br>
手动指定初始容量，也不会破坏2次幂的设计，因为HashMap的源码里通过tableSizeFor()方法进行优化  

```java
    static final int tableSizeFor(int cap) {
            // cap-1后，n的二进制最右一位肯定和cap的最右一位不同，即一个为0，一个为1，例如cap=17（00010001），n=cap-1=16（00010000）
            int n = cap - 1;
            // n = (00010000 | 00001000) = 00011000
            n |= n >>> 1;
            // n = (00011000 | 00000110) = 00011110
            n |= n >>> 2;
            // n = (00011110 | 00000001) = 00011111
            n |= n >>> 4;
            // n = (00011111 | 00000000) = 00011111
            n |= n >>> 8;
            // n = (00011111 | 00000000) = 00011111
            n |= n >>> 16;
            // n = 00011111 = 31
            // n = 31 + 1 = 32, 即最终的cap = 32 = 2 的 (n=5)次方
            return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
        }
```

### 5、负载因子是什么？为什么是0.75

> 核心思路: 不要使hashmap变成链表，不要让单节点长度超过8

扩容发生在 size = capacity * 负载因子时。  
负载因子值的选取， 其实是空间利用率Vs查询的时间 的一个取舍  
(和大多数数据结构一样，要么空间换时间，要么时间换空间)

HashMap源码的注释

```java
     * Ideally, under random hashCodes, the frequency of
     * nodes in bins follows a Poisson distribution
     * (http://en.wikipedia.org/wiki/Poisson_distribution) with a
     * parameter of about 0.5 on average for the default resizing
     * threshold of 0.75, although with a large variance because of
     * resizing granularity. Ignoring variance, the expected
     * occurrences of list size k are (exp(-0.5) * pow(0.5, k) /
     * factorial(k)). The first values are:
     *
     * 0:    0.60653066
     * 1:    0.30326533
     * 2:    0.07581633
     * 3:    0.01263606
     * 4:    0.00157952
     * 5:    0.00015795
     * 6:    0.00001316
     * 7:    0.00000094
     * 8:    0.00000006
     * more: less than 1 in ten million
```

节点出现的频率在hash桶中遵循泊松分布，同时给出了桶中元素个数和概率的对照表。  
从上面的表中可以看到当桶中元素到达8个的时候，概率已经变得非常小，也就是说用0.75作为加载因子，每个碰撞位置的链表长度超过８个是几乎不可能的。

### 6、HashMap怎么解决Hash冲突的

1. 如果真的冲突了，就使用【链式地址法】, 将 冲突的节点储存在链表后端(直至转化成红黑树)  
2. 使用扰动函数，对hashCode()方法的结果进行扰动，尽量避免不均匀的hash函数的影响


### 8、为什么要在1.8引入红黑树

- 链表转换红黑树的时机
  - 如果length > 64 , 且最长链表长度>8, 就会转换成红黑树。Node节点也会转换成TreeNode
  - 如果length < 64, 就算链表长度>8, 也会先尝试扩容，然后rehash。 (因为长度较短的时候，冲突可能不是hash算法的问题，而是hash%size，其中size较小导致的) 
- 如果hash方法设计得好，hash冲突少，其实链表是不会转换成红黑树的
- 所以红黑树是为了解决：  
  极端情况下，hashMap转成单链表的时候，查询效率低下的问题。get()时间复杂度为O(n),

> 红黑树是”近似平衡“的,  牺牲了一些查找性能 但其本身并不是完全平衡的二叉树。因此插入删除操作效率略高于AVL树。



### 9、为什么要同时重写equals()和hashCode()方法

很多参考文章都说，如果没有重写hashCode(), 那么equals相同的对象，就会有不同的hash值，落在数组的不同地方，这种情况下，同一个HashMap就会存在2个这样的对象。  
**但注意，此时说的对象，是HashMap的key对象，而不是Value。** 

假设只重写了equals()方法，

1. 如果是value对象，

   - put()的时候，槽位只根据key的hashCode而定
   - hashCode不同的对象a和b ，槽位一致，后put()的会覆盖

2. 如果是key对象，
   - 两个equals()相同的key, 同时存在hashMap中
   - (因为如果key的hashCode没冲突，就不会调用equals进行对比，更不会覆盖；
   - 这样你在get()的时候就会出现歧义(很多时候会引发BUG))，例如下面的code

```java
HashMap<A, Integer> temp = new HashMap<>();

A a = new A(1);
A b = new A(2);

temp.put(a, 1);
temp.put(b, 2);

System.out.println(temp.get(a));// 结果2
System.out.println(temp.get(new A(3)));// 结果null

```



### 10、HashMap的hash()方法

> 在HashMap的注释中说明是为了防止一些实现比较差的hashCode() 方法

```java
//Java 8中的散列值优化函数
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 :(h = key.hashCode()) ^ (h >>> 16);
    //key.hashCode()为哈希算法，返回初始哈希值
}
```

其实只是做一次16位右位移异或混合

因为hashMap的size不可能特别大，一般采用默认的16.

这个时候indexFor()函数就会将 hashCode & size, 其实也就相当于只保留了hashCode的后几位

hashCode()无论实现得多么均匀，后几位重复的概率还是很大的。



所以要做【扰动】，尽量避免碰撞



### 11、Object默认的hashCode()函数

参考文档

https://blog.gavinzh.com/2018/08/23/what-is-hashcode-of-java/