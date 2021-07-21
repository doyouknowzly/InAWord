## jps

类似于Linux的ps命令，用于列举正在运行的虚拟机进程，

并显示虚拟机执行主类(main函数所在的类)名称以及这些进程的本地虚拟机唯一ID **(LVMID local virtual machine Identifier)**。



jps [-q] [-mlvV] [<hostid>]

-q：只输出LVMID，省略主类的名称。

-m：输出虚拟机进程启动时传递给主类main函数的参数

-l：输出主类的全名，如果进程执行的是jar包，输出jar路径。

-v：输出虚拟进程启动时JVM参数。



例如

```shell
jps -q

8424

5180

8268

jstat
```

