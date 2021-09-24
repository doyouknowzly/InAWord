# crontab命令



## 原理

crond是linux下用来周期性的执行某种任务或等待处理某些事件的一个守护进程，与windows下的计划任务类似，当安装完成操作系统后，默认会安装此服务工具，并且会自动启动crond进程。

crond进程每分钟会定期检查是否有要执行的任务，如果有要执行的任务，则自动执行该任务



Linux下的任务调度分为两类，系统任务调度和用户任务调度。

- 系统任务调度：系统周期性所要执行的工作，比如写缓存数据到硬盘、日志清理等。
  - 在/etc目录下有一个crontab文件，这个就是系统任务调度的配置文件。



- 用户任务调度：用户定期要执行的工作，比如用户数据备份、定时邮件提醒等。
  - 用户可以使用 crontab 工具来定制自己的计划任务。
  - 所有用户定义的crontab 文件都被保存在 /var/spool/cron目录中。其文件名与用户名一致。



## 用法

![crontab用法与实例crontab用法与实例](https://www.linuxprobe.com/wp-content/uploads/2016/09/crontab.png)



### 示例代码

通过crontab命令执行清理日志的sh文件

```shell
crontab cleanLog.sh
```



cleanLog.sh 的文件内容如下:

```shell
* 21 * * * cat /dev/null > /home/nginx/logs/access.log
```

意思是每天21点，清空access.log日志



## cron表达式

https://zhuanlan.zhihu.com/p/35629505

![img](https://pic3.zhimg.com/80/v2-7e71c082b4aa6141a35f39e60b861dba_720w.jpg)

> 6位或7位： 因为最后一位的年，是选填项



常用示例:

![](https://pic1.zhimg.com/80/v2-6091f4a10e66595b5d5a35f19ad807bc_720w.jpg)

> 一小时一次是  0 0 1/1 * * ? ，而不是 * * 1/1 * * ?，后者会每一秒都执行
