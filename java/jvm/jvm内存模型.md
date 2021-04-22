## 

| 序号 | 问题         |
| ---- | ------------ |
| 0    | jvm内存模型  |
| 1    | 堆的结构详解 |

### 1. jvm 内存模型

根据java虚拟机规范，java虚拟机管理的内存将分为几个不同的区域， JDK1.8改动很大，所以要分开说




| 内存区域      | 线程私有性 | 作用                             |
| ------------- | ---------- | -------------------------------- |
| 堆            | 共享       | 存储“⼏乎”所有的对象、数组的地方 |
| 方法区/元空间 | 共享       | 静态变量、静态方法               |
| 直接内存      | 共享       |                                  |
| 程序计数器    | 私有       |                                  |
| 虚拟机栈      | 私有       |                                  |
| 本地方法栈    | 私有       |                                  |


**JDK1.8之前**  
![image.png](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/0122ffd4f4da47969075f0516bbac36c~tplv-k3u1fbpfcp-watermark.image)







**JDK1.8** 

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/fa5f0c96fa664673a22e13d8ff576aaa~tplv-k3u1fbpfcp-watermark.image)  
JDK 8 版本之后⽅法区被彻底移除了（JDK1.7 就已经开始了），取⽽代
之是元空间，元空间使⽤的是直接内存。  





### 2. 堆的结构详解
在 JDK 1.7 及以前，堆内存被通常被分为下⾯三部分：
1. 新⽣代内存(Young Generation)
2. ⽼⽣代(Old Generation)
3. 永久代(Permanent Generation)
![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/95b8be298f444cf09074e5603da5b6e2~tplv-k3u1fbpfcp-watermark.image)  
**JDK1.8之后，永久代被取消，变成元空间**
> 上图只是jvm的规范标准， 各个虚拟机的实现不尽相同。比如hotSpot就将方法区用作永久代，也是能满足规范的

![image.png](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/d94d5aac2f3e47529ddfebe0802a6c41~tplv-k3u1fbpfcp-watermark.image)

上图所示的 Eden 区、两个 Survivor 区都属于新⽣代（为了区分，这两个 Survivor 区域按照顺
序被命名为 from 和 to），中间⼀层属于⽼年代。

⼤部分情况，对象都会⾸先在 Eden 区域分配，在⼀次新⽣代垃圾回收后，如果对象还存活，则
会进⼊ s0 或者 s1，并且对象的年龄还会加 1(Eden 区->Survivor 区后对象的初始年龄变为 1)，
当它的年龄增加到⼀定程度（默认为 15 岁），就会被晋升到⽼年代中。对象晋升到⽼年代的年
龄阈值，可以通过参数 -XX:MaxTenuringThreshold 来设置。