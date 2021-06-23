# SDS

**SDS本质上就是char \***，因为有了表头**sdshdr**结构的存在，所以SDS比传统C字符串在某些方面更加优秀，并且能够兼容传统C字符串



sds在Redis中是实现字符串对象的工具，并且完全取代char*..sds是**二进制安全**的，它可以存储任意二进制数据，不像C语言字符串那样以‘\0’来标识字符串结束。

> 因为传统**C字符串**符合ASCII编码，这种编码的操作的特点就是：**遇零则止** 。即，当读一个字符串时，只要遇到’\0’结尾，就认为到达末尾，就忽略’\0’结尾以后的所有字符。因此，如果传统字符串保存图片，视频等二进制文件，操作文件时就被截断了。



### 3.2版本之前的SDS

![img](https://img2020.cnblogs.com/blog/1477786/202006/1477786-20200606160109497-559407668.jpg)





### 3.2版本之后的SDS

```c++
struct __attribute__ ((__packed__)) sdshdr5 {
    unsigned char flags; /* 3 lsb of type, and 5 msb of string length */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr8 {
    uint8_t len; /* used */
    uint8_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr16 {
    uint16_t len; /* used */
    uint16_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr32 {
    uint32_t len; /* used */
    uint32_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr64 {
    uint64_t len; /* used */
    uint64_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
```

![graphviz-5fccf03155ec72c7fb2573bed9d53bf8f8fb7878](https://img2018.cnblogs.com/blog/1301290/201904/1301290-20190420105230080-1708767435.png)



总结下**sds的特点**是：

- **可动态扩展内存**
- **二进制安全**
- **快速遍历字符串** 
- **与传统的C语言字符串类型兼容**





## 存储格式， embstr 和 row

而Redis 的字符串共有两种存储方式，在长度特别短时，使用 emb 形式存储 (**embedded**)，当长度超过 **44** 时，使用 **raw** 形式存储。

- **embstr**  **RedisObject 对象头和 SDS 对象连续存在一起**，使用 malloc 方法一次分配。

- 而 **raw** 存储形式不一样，它**需要两次 malloc，两个对象头在内存地址上一般是不连续的**。