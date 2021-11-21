# redis集群模式常见问题



## 一、1个节点down掉，redis怎么处理

1. 各个节点定期互相Ping(自己的Ping命令，不是TCP的Ping), 如果节点7000Ping不通,

   就将本地缓存的节点7000的ClusterNode对象标记其为PFAIL(疑似下线状态) 

2. 各个节点互相还会同步自己的缓存；同时将其他节点节点对7000的状态存在ClusterNode的一个链表里 

3. 如果一个集群中，过半的主节点都认为7000疑似下线了，就会有一个节点标记7000为FAIL下线，并发广播通知；

   其他收到广播的节点也会将其标记为FAIL下线

## 二、故障转移

一、当7000的一个从节点发现7000处于FAIL状态了，就会通知其他主节点，其他主节点就会在所有7000的从节点内**选一个作为主节点(即选举)**

二、然后将主节点的槽全部指派给自己 三、向集群发一条广播的PONG消息，通知其他节点自己是主节点啦



## 三、选举主节点

选举算法是基于Raft的领头选举的

1.每个slave会与自己的master通讯，当slave发现自己的master变为fail时。每个slave都会参与竞争，推举自己为master。
2.增加currentEpoch的值，并且每个slave向集群中的其他所有节点广播FAILOVER_AUTH_REQUEST。
3.其他master会受到多个slave的广播，但是只会给第一个slave回复FAILOVER_AUTH_ACK。
4.slave接收到ack之后，会使用过半机制开始统计。即：当前有多少master给自己ack，如果超过一半的master发送ack，则成为master。
5.广播PONG，通知给集群中的其节点。

如果没有过半的，就重新选举，直到过半 。

至此，选举流程结束。



### Redis集群中，为什么Master的数量要使用奇数？使用偶数是否可以？

> 答案是可以。使用奇数的目的：【节约 资源】
>
> 因为采用过半机制的选举流程，在高可用方面来说，奇数与偶数是一致的。
> 例如：
> 在9个master的架构中，如果4台master故障，通过过半机制，redis可以选举新的master。如果5台master故障无法选举新的master
> 在10个master的架构中，如果4台master故障，通过过半机制，redis可以选举新的master。如果5台master故障无法选举新的master



## 四、Node间的命令

- Meet

- Ping

  每个Node每秒去像本地缓存的集群其他节点进行Ping,确保其他人的存活

- PongFail

- Publish

- Moved