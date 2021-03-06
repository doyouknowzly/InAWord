# Redis高可用

[toc]

Redis高可用的发展历史

- 主从同步
- Sentinel
- Cluster集群模式



## 一、主从同步

**![](https://img2018.cnblogs.com/blog/1481291/201809/1481291-20180925142118041-1727225479.png)

Redis中的节点分为主、从节点。**主节点写，从节点读**

1. 主节点会异步将数据同步到从节点，不阻塞主节点写入

2. 如果某个主节点不响应Ping了，就会在集群内选举其从节点的一个，作为新的主节点。负责之前的槽位，[选举算法基于Raft]

   

   

复制的策略有：增量同步、快照同步、无盘复制。

1. 大部分时候都是正常的，主、从之间使用增量同步；
   - 但是如果忽然网络不好，导致几秒钟的数据没有同步。
   - 等到网络恢复的时候，再使用增量同步肯定不行
   
2. 网络恢复以后，要使用更复杂的快照同步
   - 先使用bgsave，将主节点的数据快照到磁盘
   - 然后将磁盘数据通过网络完整地传给从节点
   - 从节点接受完毕后，要清除自己的数据，然后加载刚才同步的数据
   
   
   
   > 缺点：1、无法保证高可用 2、没有解决 master 写的压力



## 二、Sentinel

在 Redis 3.0 之前，只能使用 哨兵（sentinel）机制来监控各个节点之间的状态。哨兵节点只能作监控使用，本质是额外启动哨兵节点去监控数据节点。

![img](https://img2018.cnblogs.com/blog/1481291/201809/1481291-20180925142143478-1454265814.png)

> 特点：
>
> 1、保证高可用
>
> 2、监控各个节点
>
> 3、自动故障迁移
>
> 缺点：仍然是主从模式，切换需要时间丢数据
>
> 没有解决 master 写的压力





## 三、Cluster集群模式

从redis 3.0之后版本支持redis-cluster集群，Redis-Cluster采用无中心结构，每个节点保存数据和整个集群状态,每个节点都和其他所有节点连接。

### 特点：

1. 无中心架构（不存在哪个节点影响性能瓶颈），少了 proxy 层。
2. 数据按照 slot 存储分布在多个节点，节点间数据共享，可动态调整数据分布。
3. 可扩展性，可线性扩展到 1000 个节点，节点可动态添加或删除。
4. 高可用性，部分节点不可用时，集群仍可用。通过增加 Slave 做备份数据副本
5. 实现故障自动 failover，节点之间通过 gossip 协议交换状态信息，用投票机制完成 Slave到 Master 的角色提升。



### 缺点：

1. 资源隔离性较差，容易出现相互影响的情况。
2. 数据通过异步复制,不保证数据的强一致性

### 关键点

1. 主节点负责写，从节点只能读，且会同步来自主节点的命令
2. 使用cluster meet命令将节点连接
3. 通过Gossip协议来交换各自关于不同节点的状态信息
4. 数据分片,16384(1024\*2\*8)个槽，数据结构是bitmap,每一位表示一个槽。每个主-从节点负责一部分槽, 使用CRC16(key)&16384来决定key的归属



## 四、codis vs Twemproxy

参考文档 https://blog.csdn.net/mingongge/article/details/114297675

Redis 在 3.0 的时候,推出了一个集群解决方案: redis-cluster. 能让我们通过官方的方式构建我们的redis集群

但如果使用的是redis 2.x 版本的实例, 需要进行集群管理,  采用的方案就一般是 **twitter的Twemproxy** 或者**豌豆荚的codis**



> Twemproxy 本身是一个静态的分布式方案，进行扩容、缩容的时候对我们devops的要求很高，
>
> 而且很难得做到平滑的扩容、缩容。而且没有用于集群管理的 Dashboard，这样十分不便

![img](https://img-blog.csdnimg.cn/img_convert/67b143542d417a6e272de151875b6acf.png)

codis主要是采用golang开发，而且依赖zk或etcd进行配置管理的
