# SOLID



实际上，SOLID 原则并非单纯的 1 个原则，而是由 5 个设计原则组成的，

它们分别是：单一职责原则、开闭原则、里式替换原则、接口隔离原则和依赖反转原则，依次对应 SOLID 中的 S、O、L、I、D 这 5 个英文字母



## 单一职责原则 

(Single Responsibility Principle，缩写为 SRP)

这个原则的英文描述是这样的：A class or module should have a single responsibility。

如果我们把它翻译成中文，那就是：**一个类或者模块只负责完成一个职责（或者功能）**。



实践上的经验是: 

我们可以先写一个**粗粒度**的类，满足业务需求。随着业务的发展，如果粗粒度的类越来越庞大，代码越来越多，这个时候，我们就可以将这个粗粒度的类，拆分成几个更细粒度的类。这就是所谓的**持续重构**



## 开闭原则

开闭原则是 SOLID 中最难理解、最难掌握，同时也是最有用的一条原则。

开闭原则的英文全称是 Open Closed Principle，简写为 OCP。

它的英文描述是：software entities (modules, classes, functions, etc.) should be open for extension , but closed for modification。

我们把它翻译成中文就是：软件实体（模块、类、方法等）应该“对扩展开放、对修改关闭”。

