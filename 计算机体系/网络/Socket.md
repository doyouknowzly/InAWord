## Socket

| 序号 | 问题             | 一句话描述                                                   |
| ---- | ---------------- | ------------------------------------------------------------ |
| 0    | 什么是套接字     | 是支持TCP/IP网络通信的基本操作单元，用于区分不同应用程序进程间的网络通信和连接 |
| 1    | 套接字和fd的关系 | fd：fild descriptor，就是一个文件描述器<br>在UNIX中的一切事物都是文件（everything in Unix is a file!），所以套接字也是一个文件<br> |
| 2    | 套接字格式       |                                                              |



### 1. 套接字和fd的关系

fd：fild descriptor，就是一个文件描述器。

**在UNIX中的一切事物都是文件（everything in Unix is a file!）**，所以套接字也是一个文件

我们用int在描述socket，实际上，所有的文件描述符都是int

文件是应用程序与系统（包括特定硬件设备）之间的桥梁，而文件描述符就是应用程序使用这个“桥梁”的接口。

在需要的时候，应用程序会向系统申请一个文件，然后将文件的描述符返回供程序使用。

返回socket的文件通常被创建在/tmp或者/usr/tmp中。我们实际上不用关心这些文件，仅仅能够利用返回的socket描述符就可以了。