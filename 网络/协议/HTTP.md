### Http协议
| 序号 | 问题                          |
| ---- | ----------------------------- |
| 0    | 跨域问题                      |
| 1    | Http长、短连接，和TCP有啥关系 |
| 2    | Cookie原理                    |
| 3    | Session                       |

## 2. HTTP协议 
- 跨域问题
	- 什么是跨域？
	- 解决方案
    	- `jsonp (JSON with Padding)`
        	- 原理：利用script标签的 src 连接可以访问不同源的特性，加载远程返回的“JS 函数”来执行的。
            - 缺点：只能 get 方式，易受到 XSS攻击
        - `CORS（Cross-Origin Resource Sharing）,跨域资源共享`
        	- 原理: 当使用XMLHttpRequest发送请求时，如果浏览器发现违反了同源策略就会自动加上一个请求头 origin；
				后端在接受到请求后确定响应后会在后端在接受到请求后确定响应后会在 Response Headers 中加入一个属性 Access-					Control-Allow-Origin；
			- 浏览器判断响应中的 Access-Control-Allow-Origin 值是否和当前的地址相同，匹配成功后才继续响应处理，否则报错
        - 基于 `Html5 websocket 协议`.
        	- websocket 是 Html5 一种新的协议，基于该协议可以做到浏览器与服务器全双工通信，允许跨域请求
        	- 缺点：浏览器一定版本要求，服务器需要支持 websocket 协议  
                


## 3. HTTPS协议
- 目的：  
    解决http协议的安全性问题
    - 请求信息明文传输，容易被窃听截取
    - 数据的完整性未校验，容易被篡改
    - 不验证通讯方身份，有可能会遭遇伪装
- 端口：  
    使用443
- 定义：  
    HTTPS 协议（HyperText Transfer Protocol over Secure Socket Layer）：  
    【安全套接字层上面的超文本传输协议】  
一般理解为HTTP+SSL/TLS，通过SSL证书来验证服务器的身份，并为C/S之间的通信进行加密。
    
- 思路：HTTPS = HTTP + 加密 + 认证 + 完整性保护  
    在 HTTP 的部分通信接口采用 SSL 和 TLS 协议替代，使用了数字证书认证机构和其他相关机关颁发的公开秘钥证书。
    

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/6a76ec79992f4a87ac80179e008f9a94~tplv-k3u1fbpfcp-watermark.image)

- 详细参考 [全面理解HTTP&HTTPS协议](https://juejin.cn/post/6844904006737723399)