# String



### 1. String, StringBuilder, StringBuffer区别

- String的值是不可变的
  - 这就导致每次对String的操作都会生成**新的String对象**, 效率低下且浪费空间
  - 为什么不可变呢？ 因为默认使用指针指向常量池的字符串对象， 而不是在堆里
  - 如果预期到字符串会频繁变更，就要有意识地使用StringBuilder和StringBuffer
- StringBuilder线程不安全但性能快 ，大多数场景使用StringBuilder
  - 使用 char[]实现
  - 默认初始化长度是16个char
  - 扩容的时候，先扩容至 当前size * 2 + 2的长度
    -  如果不够，再使用append之后的字符串长度作为数组长度
- StringBuffer线程安全
  - 使用synchronized修饰方法



![img](https://img-blog.csdn.net/20180411091757991?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTEwMTE3Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

