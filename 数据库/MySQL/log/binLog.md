# bin log

1. 作用

   **binlog(归档日志) 是逻辑日志**, 存储的是每一条SQL 

   逻辑的意思是，迁移到其他MySQL实例上也行，即使其他的是MyISAM。

   主要作用:**备份恢复and主从复制**

2. 格式

   3种格式， 一般推荐使用row格式

   - row : 基于行的模式，记录的是行的变化，很安全
   - statement : 基于SQL语句的模式，某些语句中含有一些函数，例如 UUID NOW 等在复制过程可能导致数据不一致甚至出错
   - mixed : 混合模式，根据语句来选用是 statement 还是 row 模式

3. 关联

   redo log 和 binlog 有一个共同的数据字段叫 **XID**。崩溃恢复的时候会按顺序扫描 redo log。<br/>如果碰到既有 prepare、又有 commit 的 redo log就直接提交<br/>如果碰到只有 parepare、而没有 commit 的 redo log就拿着 XID 去 binlog 找对应的事务。