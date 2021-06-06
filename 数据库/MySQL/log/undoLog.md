## undo log

1. undo log的作用

   **undo log一般是逻辑日志，根据每行记录进行记录**<br>用来在**事务**中回滚行记录到某个版本。

2. undolog和redo log的关系

   **undo log**也会产生redo log

3. 多版本控制

   InnoDB的多版本使用undo log来构建， 这很好理解，undo log 中包含了记录更改前的镜像，

   如果更改数据的事务未提交，对于隔离级别大于等于read commit的事务而言，它不应该看到已修改的数据，而是应该给它返回老版本的数据。

