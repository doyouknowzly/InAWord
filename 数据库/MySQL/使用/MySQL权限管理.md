# MySQL权限管理



mysql中存在4个控制权限的表，分别为

- user表
- db表
- tables_priv表
- columns_priv表

权限存储在这几个系统表中，待MySQL实例启动后就加载到内存中

## 一、权限验证流程

1. 先从user表中的Host,User,Password这3个字段中判断连接的ip、用户名、密码是否存在，存在则通过验证。
2. 通过身份认证后，进行权限分配，按照user，db，tables_priv，columns_priv的顺序进行验证。
3. 先检查全局权限表user，如果user中对应的权限为Y，则此用户对所有数据库的权限都为Y，将不再检查db, tables_priv,columns_priv；
4. 如果为N，则到db表中检查此用户对应的具体数据库，并得到db中为Y的权限；
5. 如果db中为N，则检查tables_priv中此数据库对应的具体表，取得表中的权限Y
6. 以此类推。



## 二、常用SQL

1. user表查询

   select  *  from mysql.user where user like "%你的username%";

   select  user, host, password  from mysql.user where user like "%你的username%";

   

2. db表查询

   select  db,insert_priv   from mysql.db where user like "%你的username%";

