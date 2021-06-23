## windows环境

https://blog.csdn.net/laixiaonian/article/details/91900328



1、下载windows版本的openresty：

http://openresty.org/cn/download.html

2、解压

启动nginx.exe：

双击nginx.exe运行 



3、验证：

方式一、打开控制台执行命令：

tasklist /fi "imagename eq nginx.exe"

![img](https://img-blog.csdnimg.cn/2019061322020843.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xhaXhpYW9uaWFu,size_16,color_FFFFFF,t_70)

方式二、登陆网址：

http://127.0.0.1:80/

![img](https://img-blog.csdnimg.cn/20190613220243831.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xhaXhpYW9uaWFu,size_16,color_FFFFFF,t_70)

注：可以到nginx.conf中listen的参数修改端口

