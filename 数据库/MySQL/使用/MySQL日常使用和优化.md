# 日常使用

| 序号 | 问题                           | 一句话解释 | 详细知识点 |
| ---- | ------------------------------ | ---------- | ---------- |
| 0    | 怎么定位慢SQL                  |            |            |
| 1    | 怎么处理慢SQL                  |            |            |
| 2    | explain语句怎么用              |            |            |
| 3    | 分库分表                       |            |            |
| 4    | 触发器是什么，什么场景下使用？ |            |            |



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

