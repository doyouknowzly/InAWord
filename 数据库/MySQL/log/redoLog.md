## redo log

1. 作用

   **redo log通常是物理日志**，记录的是数据页的物理修改，而不是某一行或某几行修改成怎样怎样。它用来**在崩溃后恢复<br>

   - 1、**增加服务的吞吐**，因为写日志是增量追加，很快啊 <br>
   - 2、**高可用**，即使服务重启、死掉，也可以从redo log 恢复，称为 **crash-safe**
     - 注意:**redo log 是InnoDb引擎引入的，Server层并没有redo log**，即MyISAM引擎并没有**crash-safe**能力<br>
     - 恢复是恢复到commit后的物理数据页**(恢复数据页，且只能恢复到最后一次提交的位置)

2. 格式

   - MySQL redo log，默认配置下有两个文件，分别是ib_logfile0和ib_logfile1，这两个文件有完全相同的格式

   - redo log 文件最小单位是512字节的一个块，每个块的最后4个字节，存储这个块的checksum校验值

   - redo log 文件前4个块，也就是前2048个字节为文件头，文件头存储了redo log文件元数据信息和checkpoint信息

   - 整体来看redo log文件格式如下：

     ```mysql
        0 --------------------------------
                 log file header block
     512 ---------------------------------
                 checkpoint block1
     1024--------------------------------
                 5.7保留，8.0用于加密
     1536--------------------------------
                 checkpoint block2
     2048--------------------------------
                 redo log record ...
     xxxxx--------------------------------
     ```

     参考文档[MySQL redo log 格式解析](http://www.weijingbiji.com/2183/)

3. 写入过程

   写redo log的方式，是WAL技术，即Write-Ahead Logging, 核心就是:**先写日志，再更新磁盘文件**

   因为磁盘文件更新很慢，要定位、磁盘寻址、修改，所以就先记在redo log上，有空的时候再更新。

   所以， MySQL定义的insert\update语句执行完成就是: **先写入redo log, 再更新内存，就算完成**(刷新磁盘的事不着急，慢慢刷)

   

   其实redo log的写入过程就是**2阶段提交(2PC)**.

   - 执行器调用引擎写入数据，写到了redo log
   - redo log写入后，处于prepare状态 
   - 执行器生成binlog,并写入磁盘 
   - 执行器调用引擎接口提交，引擎将redo log的状态流转，从prepare -> commit

   ![img](https://www.linuxidc.com/upload/2018_11/181121105137361.jpg)

   > 图片来自极客时间，该图展示了一组4个文件的redo log日志，checkpoint之前表示擦除完了的，即可以进行写的，擦除之前会更新到磁盘中，write pos是指写的位置，当write pos和checkpoint相遇的时候表明redo log已经满了，这个时候数据库停止进行数据库更新语句的执行，转而进行redo log日志同步到磁盘中。

4. redo log 写入过程中如果宕机了，怎么办？

   1. prepare阶段 

   2. 写binlog 

   3. commit

   **当在2之前崩溃时**,重启恢复：发现没有commit，回滚。

   备份恢复：没有binlog 。和崩溃前一致

   **当在3之前崩溃**重启恢复：虽没有commit，但满足prepare和binlog完整，所以重启后会自动commit.

   备份恢复：有binlog. 一致