参考文档 : https://blog.huoding.com/2010/10/10/8

> OAuth授权的核心 :

==颁发==访问令牌(Token)、使用访问令牌



## 一、什么是OAuth

如今很多网站的功能都强调彼此间的交互，因此我们需要一种简单，标准的解决方案来安全的完成应用的授权，于是，OAuth应运而生，看看官网对其的定义：

> An open protocol to allow secure API authorization in a simple and standard method from desktop and web applications.

一个典型的OAuth应用通常包括三种角色，分别是：

- Consumer：消费方
- Service Provider：服务提供者
- User：用户





## 二、历史


2007年12月4日发布了OAuth Core 1.0：

此版本的协议存在严重的安全漏洞：OAuth Security Advisory: 2009.1，更详细的介绍可以参考：Explaining the OAuth Session Fixation Attack。



2009年6月24日发布了OAuth Core 1.0 Revision A：

此版本的协议修复了前一版本的安全漏洞，并成为RFC5849，我们现在使用的OAuth版本多半都是以此版本为基础。



## 三、使用 

消费方如果想使用服务提供者的OAuth功能，通常需要先申请两样东西：

- Consumer Key
- Consumer Secret

当消费方生成签名的时候，会用到它们。



一个典型的OAuth流程通常如下图所示：

![OAuth流程图](https://blog.huoding.com/wp-content/uploads/2010/10/oauth_flow.png)

- A：消费方请求Request Token
- B：服务提供者授权Request Token
- C：消费方定向用户到服务提供者
- D：获得用户授权后，服务提供者定向用户到消费方
- E：消费方请求Access Token
- F：服务提供者授权Access Token
- G：消费方访问受保护的资源



基本就是用Request Token换取Access Token的过程。

这里需要注意的是，对服务提供者而言，Request Token和Access Token的生命周期不一样，通常，Request Token的生命周期很短，一般在一个小时以内，这样相对安全一些；而Access Token的生命周期很长，往往是无限。

如此一来，消费方就可以把它保存起来，以后的操作就无需用户再授权了，即便用户修改账号密码，也不会受影响，当然，用户可以废除消费方的授权。



## 四、Oauth和OpenId的对比

OpenID：Authentication 认证

OAuth ：Authorization  授权

<img src="https://img-blog.csdn.net/20180330104507855" style="zoom: 33%;" />

在进入到QQ登录界面后，最开始是要请求认证，用户输入QQ号和密码，点击登录，腾讯互联会先进行验证该用户是否为我的用户，如果是我的用户，那么我会通知你（CSDN），他是我的用户，你可以使用该账户登录你的系统，这个过程就是认证（Authentication），认证就是证明你是谁，你是否是真实存在的，就好像，快递员来给你送快递，让你出示你的身份证，他确定你是本人后，把快递给你，这就是OpenID。



而在QQ授权登录下方，有两给CheckBox复选框，可以允许CSDN获得您的昵称、头像、性别，这是在认证之后的事了，在腾讯互联你是我平台的用户后，你可以自己选择CSDN是否有权去获取你的相关信息，当你勾选后，腾讯互联就把你的这些基本信息给了CSDN，这个过程就是授权（Authorization），授权就是确定了你是谁后，又把属于你的东西给了别人