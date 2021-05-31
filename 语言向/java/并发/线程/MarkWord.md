# MarkWord



## 一、定义

根据jvm的分区，对象分配在堆内存中，可以用下图表示：
![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly93d3cubGludXhpZGMuY29tL3VwbG9hZC8yMDE4XzAyLzE4MDIwNjIxNTM3MjMzMS5wbmc?x-oss-process=image/format,png)



### 对象头

Hotspot虚拟机的对象头包括两部分信息，第一部分用于储存对象自身的运行时数据，如哈希码，GC分代年龄，锁状态标志，锁指针等，这部分数据在32bit和64bit的虚拟机中大小分别为32bit和64bit，官方称它为"Mark word",考虑到虚拟机的空间效率，Mark Word被设计成一个非固定的数据结构以便在极小的空间中存储尽量多的信息，它会根据对象的状态复用自己的存储空间，详细情况如下图：
![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly93d3cubGludXhpZGMuY29tL3VwbG9hZC8yMDE4XzAyLzE4MDIwNjIxNTM3MjMzMTEucG5n?x-oss-process=image/format,png)



### Monitor

通常所说的对象的内置锁，是对象头Mark Word中的重量级锁指针指向的monitor对象，该对象是在HotSpot底层C++语言编写的(openjdk里面看)

```c++

//结构体如下
ObjectMonitor::ObjectMonitor() {  
  _header       = NULL;  
  _count       = 0;  
  _waiters      = 0,  
  _recursions   = 0;       //线程的重入次数
  _object       = NULL;  
  _owner        = NULL;    //标识拥有该monitor的线程
  _WaitSet      = NULL;    //等待线程组成的双向循环链表，_WaitSet是第一个节点
  _WaitSetLock  = 0 ;  
  _Responsible  = NULL ;  
  _succ         = NULL ;  
  _cxq          = NULL ;    //多线程竞争锁进入时的单向链表
  FreeNext      = NULL ;  
  _EntryList    = NULL ;    //_owner从该双向循环链表中等待资源的线程结点，_EntryList是第一个节点
  _SpinFreq     = 0 ;  
  _SpinClock    = 0 ;  
  OwnerIsThread = 0 ;  

```

