参考文档: https://www.zhihu.com/question/20400700



## 1. 目的

当需要存放任意类型时，泛型可以帮助我们在编译期检查，避免类型不匹配导致的object转换失败问题



## 2. 流程

1、在编译期间，泛型有效，编译器会帮助我们检查Class的类型。

2、编译期后，jvm会将类型信息擦除，并且在对象进入和离开方法的边界处添加类型检查和类型转换的方法



## 3. 使用场景

1、泛型类

通过泛型可以完成对一组类的操作对外开放相同的接口。最典型的就是各种容器类，如：List、Set、Map

一个最普通的泛型类：

```java
//此处T可以随便写为任意标识，常见的如T、E、K、V等形式的参数常用于表示泛型
//在实例化泛型类时，必须指定T的具体类型
public class Generic<T>{ 
    //key这个成员变量的类型为T,T的类型由外部指定  
    private T key;

    public Generic(T key) { //泛型构造方法形参key的类型也为T，T的类型由外部指定
        this.key = key;
    }

    public T getKey(){ //泛型方法getKey的返回值类型为T，T的类型由外部指定
        return key;
    }
}
```





2、泛型接口

泛型接口与泛型类的定义及使用基本相同。泛型接口常被用在各种类的生产器中，可以看一个例子：

```java
/**
 * 未传入泛型实参时，与泛型类的定义相同，在声明类的时候，需将泛型的声明也一起加到类中
 * 即：class FruitGenerator<T> implements Generator<T>{
 * 如果不声明泛型，如：class FruitGenerator implements Generator<T>，编译器会报错："Unknown class"
 */
class FruitGenerator<T> implements Generator<T>{
    @Override
    public T next() {
        return null;
    }
}
```

当实现泛型接口的类，传入泛型实参时：

```java
/**
 * 传入泛型实参时：
 * 定义一个生产器实现这个接口,虽然我们只创建了一个泛型接口Generator<T>
 * 但是我们可以为T传入无数个实参，形成无数种类型的Generator接口。
 * 在实现类实现泛型接口时，如已将泛型类型传入实参类型，则所有使用泛型的地方都要替换成传入的实参类型
 * 即：Generator<T>，public T next();中的的T都要替换成传入的String类型。
 */
public class FruitGenerator implements Generator<String> {

    private String[] fruits = new String[]{"Apple", "Banana", "Pear"};

    @Override
    public String next() {
        Random rand = new Random();
        return fruits[rand.nextInt(3)];
    }
}
```



3、泛型方法



## 4. 泛型通配符

为什么要有通配符

> 容器里装的东西之间有继承关系，但容器之间是没有继承关系的

使用泛型的过程中，经常出现一种很别扭的情况。我们有*Fruit*类，和它的派生类*Apple*类。

```java
class Fruit {}
class Apple extends Fruit {}
```

然后有一个最简单的容器：*Plate*类。盘子里可以放一个泛型的“*东西*”。我们可以对这个东西做最简单的“*放*”和“*取*”的动作：*set( )*和*get( )*方法。

```java
class Plate<T>{
    private T item;
    public Plate(T t){item=t;}
    public void set(T t){item=t;}
    public T get(){return item;}
}
```

现在我定义一个“*水果盘子*”，逻辑上水果盘子当然可以装苹果。

```java
Plate<Fruit> p=new Plate<Apple>(new Apple());
```

但实际上Java编译器不允许这个操作。会报错，“*装苹果的盘子*”无法转换成“*装水果的盘子*”。

```java
error: incompatible types:Plate<Apple> cannot be converted to Plate<Fruit>
```

所以我的尴尬症就犯了。实际上，编译器脑袋里认定的逻辑是这样的：

- 苹果 ***IS-A\*** 水果
- 装苹果的盘子 ***NOT-IS-A\*** 装水果的盘子

所以，**就算容器里装的东西之间有继承关系，但容器之间是没有继承关系的**.

所以我们不可以把*Plate<Apple>*的引用传递给*Plate<Fruit>*。



为了让泛型用起来更舒服，Sun的大脑袋们就想出了<? extends T>和<? super T>的办法，来让”*水果盘子*“和”*苹果盘子*“之间发生关系。



### 4.1 上界通配符

<? extends T>：是指 **“上界通配符（Upper Bounds Wildcards）”**

```java
Plate<？ extends Fruit>
```

**一个能放水果以及一切是水果派生类的盘子**

![img](https://pic2.zhimg.com/80/cdec0a066693684036d4bcaab4fdc1e3_720w.jpg?source=1940ef5c)

### 4.2 下界通配符

<? super T>：是指 **“下界通配符（Lower Bounds Wildcards）”**

```java
Plate<？ super Fruit>
```

表达的就是相反的概念：**一个能放水果以及一切是水果基类的盘子**

![img](https://pic3.zhimg.com/80/0800ab14b2177e31ee3b9f6d477918fa_720w.jpg?source=1940ef5c)



## 来自知乎评论的另一种理解思路

java是单继承，所有继承的类构成一棵树。
假设A和B都在一颗继承树里（否则super，extend这些词没意义）。
A super B 表示A是B的父类或者祖先，在B的上面。
A extend B 表示A是B的子类或者子孙，在B下面。

由于树这个结构上下是不对称的，所以这两种表达区别很大。假设有两个泛型写在了函数定义里，作为函数形参（形参和实参有区别）：

1. 参数写成：T<? super B>，对于这个泛型，?代表容器里的元素类型，由于只规定了元素必须是B的超类，导致元素没有明确统一的“根”（除了Object这个必然的根），所以这个泛型你其实无法使用它，对吧，除了把元素强制转成Object。所以，对把参数写成这样形态的函数，函数体内，

   **只能对这个泛型做插入操作，而无法读**

2. 参数写成： T<? extends B>，由于指定了B为所有元素的“根”，你任何时候都可以安全的用B来使用容器里的元素，但是插入有问题，由于供奉B为祖先的子树有很多，不同子树并不兼容，由于实参可能来自于任何一颗子树，所以你的插入很可能破坏函数实参，所以，对这种写法的形参，

  **禁止做插入操作，只做读取**

