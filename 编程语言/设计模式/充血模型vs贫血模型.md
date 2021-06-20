# 充血模型vs贫血模型

参考文章 (https://time.geekbang.org/column/article/169631)

### 贫血模型

常见的MVC设计模式，即Controller、Service、Repository， 很多web服务都是这么写的，BO\VO\Model等实体只用作数据存储，

业务逻辑都写在Service层里



缺点是：

- 面向过程，而不是面向对象
- service层特别冗长
- 如果逻辑越来越复杂，扩展性不好，修改起来困难



### 充血模型

Controller、Repository 因为逻辑不多，所以仍然保持贫血模型；

Service层将BO自己的逻辑放进BO里, 让数据模型BO自己对自己复杂。

和Controller、Repository的交互代码，仍然保留在Service里



**充血模型是DDD开发模式的最佳实践， 即"领域驱动开发Domain Drive Devlopment"**, 领域对象，要对自己负责，且只负责最少、必要的功能

