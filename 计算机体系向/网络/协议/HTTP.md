### Http协议
| 序号 | 问题                          |
| ---- | ----------------------------- |
| 0    | 常见的HTTP code               |
| 1    | 跨域问题                      |
| 2    | Http长、短连接，和TCP有啥关系 |
| 3    | Cookie原理                    |
| 4    | Session                       |
|      |                               |

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
| 302  | Move Temporarily       | 临时重定向                                                   |
| 305  | Use Proxy              | 被请求的资源必须通过指定的代理才能被访问                     |
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

### 1. 跨域问题

什么是跨域？



解决方案

- `jsonp (JSON with Padding)`

  原理：利用script标签的 src 连接可以访问不同源的特性，加载远程返回的“JS 函数”来执行的。

  缺点：只能 get 方式，易受到 XSS攻击

- `CORS（Cross-Origin Resource Sharing）,跨域资源共享`

  原理: 当使用XMLHttpRequest发送请求时，如果浏览器发现违反了同源策略就会自动加上一个请求头 origin；
  后端在接受到请求后确定响应后会在后端在接受到请求后确定响应后会在 Response Headers 中加入一个属性 Access-					Control-Allow-Origin；

  浏览器判断响应中的 Access-Control-Allow-Origin 值是否和当前的地址相同，匹配成功后才继续响应处理，否则报错

- 基于 `Html5 websocket 协议`.

  websocket 是 Html5 一种新的协议，基于该协议可以做到浏览器与服务器全双工通信，允许跨域请求

  缺点：浏览器一定版本要求，服务器需要支持 websocket 协议  
      

- 详细参考 [全面理解HTTP&HTTPS协议](https://juejin.cn/post/6844904006737723399)



