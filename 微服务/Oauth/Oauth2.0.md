

## 一、对比Oauth 1.0和2.0

**OAuth**1.0虽然在安全性上经过修补已经没有问题了，但还存在其它的缺点，其中最主要的莫过于以下两点：

其一，签名逻辑过于复杂，对开发者不够友好；

其二，授权流程太过单一，除了Web应用以外，对桌面、移动应用来说不够友好。



1. 首先，去掉签名，改用SSL（HTTPS）确保安全性，所有的token不再有对应的secret存在，这也直接导致**OAuth**2.0不兼容老版本。

2. **OAuth**1.0定义了三种角色：User、Service Provider、Consumer。

   而**OAuth**2.0则定义了四种角色：Resource Owner、Resource Server、Client、Authorization Server：

   - Resource Owner：User

   - Resource Server：Service Provider

   - Client：Consumer

   - Authorization Server：Service Provider

     

   也就是说，**OAuth**2.0把原本**OAuth**1.0里的Service Provider角色分拆成Resource Server和Authorization Server两个角色，在授权时交互的是Authorization Server，在请求资源时交互的是Resource Server，当然，有时候他们是合二为一的。

     

3. 新增授权类型

   - **Authorization Code**
     - 可用范围：此类型可用于有服务端的应用，是最贴近老版本的方式。
   - **Implicit Grant**
     - 可用范围：此类型可用于没有服务端的应用，比如Javascript应用。
   - **Resource Owner Password Credentials**
     - 可用范围：不管有无服务端，此类型都可用。
   - **Client Credentials**
     - 可用范围：不管有无服务端，此类型都可用