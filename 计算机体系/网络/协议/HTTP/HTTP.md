### Http协议
| 序号 | 问题                          |
| ---- | ----------------------------- |
| 0    | 常见的HTTP code               |
| 1    | 跨域问题                      |
| 2    | Http长、短连接，和TCP有啥关系 |
| 3    | Cookie原理                    |
| 4    | Session                       |
| 5    | post请求格式                  |

## HTTP协议 

### 0.常见的HTTP code

| CODE |                        |                                                              |
| ---- | ---------------------- | ------------------------------------------------------------ |
| 200  | OK                     | 成功                                                         |
| 201  | Created                |                                                              |
| 202  | Accepted               | 服务器已接受请求，但尚未处理，一般是异步情况下使用           |
| 204  | No Content             | 成功接收并理解，就是没有内容                                 |
|      |                        |                                                              |
| 300  | Multiple Choices       | 被请求的资源有一系列可供选择的回馈信息，<br>用户或浏览器能够自行选择一个首选的地址进行重定向 |
| 301  | Moved Permanently      | 永久移动到新位置                                             |
| 302  | Move Temporarily       | 临时重定向，只使用GET                                        |
| 305  | Use Proxy              | 被请求的资源必须通过指定的代理才能被访问                     |
| 307  |                        | 补充302， 使用原请求的方法、包体，不改变                     |
| 308  |                        | 补充301，不改变方法、包体                                    |
|      |                        |                                                              |
| 400  | Bad Request            | 语义有误 \  参数有误                                         |
| 401  | Unauthorized           | 当前请求需要用户验证 or 认证失败                             |
| 403  | Forbidden              | 服务器已经理解请求，但是拒绝执行它                           |
| 404  | Not Found              | 请求失败，请求所希望得到的资源未被在服务器上发现             |
| 405  | Method Not Allowed     | 请求方法不能被用于请求相应的资源                             |
| 408  | Request Timeout        | 请求超时                                                     |
| 415  | Unsupported Media Type | Header中 Accept 的资源类型，服务器不支持                     |
|      |                        |                                                              |
| 500  | Internal Server Error  | 服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理 |
| 502  | Bad Gateway            | 作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应 |
| 504  | Gateway Timeout        | 网关OK，上游服务器超时                                       |
|      |                        |                                                              |



> 301 和 302的区别常考: 
>
> 301 是永久的，搜索引擎在抓取新内容的同时也将旧的网址替换为重定向之后的网址
>
> 302是临时的， 搜索引擎会抓取新的内容而保留旧的网址。因为服务器返回302代码，搜索引擎认为新的网址只是暂时的。
>
> 
>
> 301、302只使用GET， 而如果想保留原方法、包体，需要用308、307（百度搜索就使用的307）



### 1.跨域问题

[参考<<跨域问题>>](./跨域问题)





### 3. Http长、短连接

HTTP长连接

- 浏览器向服务器进行一次HTTP会话访问后，并不会直接关闭这个连接，而是会默认保持一段时间，那么下一次浏览器继续访问的时候就会再次利用到这个连接。
- 在`HTTP/1.1`版本中，默认的连接都是长连接，我们可以通过`Connection: keep-alive`字段进行指定。

HTTP短连接

- 浏览器向服务器每进行一次HTTP操作都要建立一个新的连接。
- 在`HTTP/1.0`版本中默认是短链接



因为HTTP本质上使用TCP/IP传输数据， 连接指的就是传输层的TCP连接

> 所以HTTP协议的长连接本质上就是TCP的长连接。



### 5.post请求格式

**常见的Body格式有**

- form-data
- x-www-form-urlencoded
- raw
- binary
- json



对比得到区别如下：

1. **x-www-form-urlencoded**

   > 是post请求的默认格式， 使用js中URLencode转码方法

   **application/x-www-form-urlencoded，会将表单内的数据转换为键值对，&分隔。**
   当form的action为get时，将表单数据编码为(name1=value1&name2=value2…)，

   然后把这个字符串append到url后面，用?分隔，跳转到这个新的url。

   当form的action为post时，浏览器将form数据封装到http body中，然后发送到server。
   这个格式不能提交文件。

2. form-data

   对于一段utf8编码的字节，用application/x-www-form-urlencoded传输其中的ascii字符没有问题，但对于非ascii字符传输效率就很低了（汉字‘丁’从三字节变成了九字节）

   >  因此在传很长的字节（如文件）时应用multipart/form-data格式

   就是Content-Type: multipart/form-data,

   它会将表单的数据处理为一条消息，以标签为单元，用分隔符分开。既可以上传键值对，也可以上传文件。当上传的字段是文件时，会有Content-Type来说明文件类型；content-disposition，用来说明字段的一些信息；

   由于有boundary隔离，所以multipart/form-data既可以上传文件，也可以上传键值对，它采用了键值对的方式，所以可以上传多个文件。

   

3. raw
   可以上传任意格式的文本，可以上传text、json、xml、html、javascript等

4. binary
   等同于Content-Type:application/octet-stream，只可上传二进制数据，通常用来上传文件，由于没有键值，所以一次只能上传一个文件

   