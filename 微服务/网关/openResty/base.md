官网 : (http://openresty.org/cn/)

## 一、OpenResty定位

OpenResty® 是一个基于 **Nginx与 Lua** 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。

用于方便地搭建能够处理**超高并发**、**扩展性极高**的动态 Web 应用、Web 服务和动态网关。



#### 优势 ：兼顾 nginx 底层C语言的高性能、高并发； 又具有Lua 的动态性 (不用重启就能动态修改代码，且Lua语法简单明了)

> nginx本身是世界份额排名第一的web服务器，Apache第二， 而OpenResty是第五

 

## 二、OpenResty组件

组件列表: (http://openresty.org/cn/components.html)

常用的有:

- Nginx
- LuaJIT
- lua-nginx-module
- resty



其中，resty是OpenResty作者用Perl写的, 1000多行客户端脚本，本质 是一堆命令行指令的封装，底层通过Nginx进程来实现各种Web功能

> 为什么是perl呢？ 因为作者章亦春偏好perl. 第一版OpenResty，就是使用的perl写的，后因性能问题转用lua



> LuaJIT是采用C语言写的Lua的解释器。LuaJIT被设计成全兼容标准Lua 5.1, 因此LuaJIT代码的语法和标准Lua的语法没多大区别。
>
> LuaJIT和Lua的一个区别是，LuaJIT的运行速度比标准Lua快数十倍，可以说是一个lua的高效率版本, 且包含很多lua没有的函数。



## 三、openResty的11个阶段指令

和nginx11个阶段类似， openResty也设置了 11 个 *_by_lua指令, 

它们和 NGINX 阶段的关系如下图所示（图片来自 lua-nginx-module 文档）：

![img](https://static001.geekbang.org/resource/image/2a/73/2a05cb2a679bd1c81b44508666e70273.png)

对于业务代码来说，其实大部分的操作都可以在 content_by_lua 里面完成，但我更推荐的做法，是根据不同的功能来进行拆分，比如下面这样：

set_by_lua：设置变量；

rewrite_by_lua：转发、重定向等；

access_by_lua：准入、权限等；c

ontent_by_lua：生成返回内容；

header_filter_by_lua：应答头过滤处理；

body_filter_by_lua：应答体过滤处理；

log_by_lua：日志记录。



举一个例子来说明这样拆分的好处。

假设，你对外提供了很多明文 API，现在需要增加自定义的加密和解密逻辑。那么请问，需要修改所有 API 的代码吗？

```nginx

# 明文协议版本
location /mixed {
    content_by_lua '...';       # 处理请求
}
```

当然不用。

事实上，利用阶段的特性，我们只需要简单地在 access 阶段解密，在 body filter 阶段加密就可以了，原来 content 阶段的代码是不用做任何修改的：

```nginx

# 加密协议版本
location /mixed {
    access_by_lua '...';        # 请求体解密
    content_by_lua '...';       # 处理请求，不需要关心通信协议
    body_filter_by_lua '...';   # 应答体加密
}
```



## 四、常用库

Lua 比较小巧，内置的标准库并不多。而且，在 OpenResty 的环境中，Lua 标准库的优先级是很低的。

对于同一个功能，优先使用 OpenResty 的 API 来解决，然后是 LuaJIT 的库函数，最后才是标准 Lua 的函数。

```java
OpenResty的API > LuaJIT的库函数 > 标准Lua的函数
```

这个优先级后面会被反复提及，它不仅关系到是否好用这一点，更会对性能产生非常大的影响
