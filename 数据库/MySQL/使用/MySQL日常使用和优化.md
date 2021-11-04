# 日常使用

| 序号 | 问题                           | 一句话解释 | 详细知识点 |
| ---- | ------------------------------ | ---------- | ---------- |
| 0    | 怎么定位慢SQL                  |            |            |
| 1    | 怎么处理慢SQL                  |            |            |
| 2    | explain语句怎么用              |            |            |
| 3    | 分库分表                       |            |            |
| 4    | 触发器是什么，什么场景下使用？ |            |            |
| 5    | count(1) 和count(*)            |            |            |



## 0.怎么定位慢SQL

show variables like '%query%'

可以看到数据库实例对查询的一些配置

其中，重点关注

slow_query_log 和 slow_query_log_file, 是慢查询日志开关，和文件存储的位置



long_query_time是超时阈值，单位是秒

```sql
long_query_time     		1.000000
slow_query_log				ON
slow_query_log_file			/rdsdbdata/log/slowquery/mysql-slowquery.log
```



## 2.explain语句怎么用

参考文档

https://zhuanlan.zhihu.com/p/111295077



```mysql
mysql> EXPLAIN SELECT * FROM t1 UNION SELECT * FROM t2;
+----+--------------+------------+------------+------+---------------+------+---------+------+------+----------+-----------------+
| id | select_type  | table      | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra           |
+----+--------------+------------+------------+------+---------------+------+---------+------+------+----------+-----------------+
|  1 | PRIMARY      | t1         | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 405 |   100.00 | NULL            |
|  2 | UNION        | t2         | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 1805 |   100.00 | NULL            |
| NULL | UNION RESULT | <union1,2> | NULL       | ALL  | NULL          | NULL | NULL    | NULL | NULL |     NULL | Using temporary |
+----+--------------+------------+------------+------+---------------+------+---------+------+------+----------+-----------------+
3 rows in set, 1 warning (0.00 sec)
```



重点关注 【type】·【possible_keys】·【key】·【rows】

分别是 select的方式、 可能用的索引、实际用的索引，预估的扫描行数



其中type:

- system：表中只有一条记录，且该表使用的存储引擎的统计数据是精确的，eg：myisam或者memory；
- const：根据主键或者唯一索引与常数进行等值匹配时；
- eq_ref：连接查询场景，被驱动表通过主键或唯一索引进行等值匹配时，被驱动表的访问方式就是eq_ref；
- ref：普通二级索引进行等值匹配时；
- fulltext：全文索引；
- ref_or_null：普通二级索引进行等值匹配或者还可以是null场景；
- index_merge：索引合并；
- unique_subquery：包含in子查询的查询，查询优化器将in子查询转化为exists子查询，且子查询可以使用主键进行等值匹配；
- index_subquery：包含in子查询的查询，查询优化器将in子查询转化为exists子查询，且子查询可以使用普通索引进行等值匹配；
- range：使用索引查询某些范围区间（单点区间、范围区间）的记录；
- index：使用索引覆盖，但需要扫描全部索引记录；
- all：全表扫描；



大部分场景，最好是const, ref,range



## 5. count(1)和count(*)

1. Count (*)和Count(1)查询结果是一样的，都包括对NULL的统计，而count(列名) 是不包括NULL的统计
2. 如果表没有主键,count(1)比count(*)快.
3. 如果有主键的话，主键作为count的条件时候count(主键)最快.
4. 如果表只有一个字段的话那count(*)就是最快的