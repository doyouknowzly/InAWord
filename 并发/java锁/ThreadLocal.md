

## ThreadLocal
### 1.简介 
对比其他解决线程安全的方案，更轻量级，开销更小，且更简单。

### 2.如何使用

```java
static ThreadLocal<A>  threadLocal= new ThreadLocal<>();

threadLocal.set(1996);
int temp = threadLocal.get();
threadLocal.remove();
```

### 3、一句话总结
- 每个Thread对象，其ThreadLocalMap都不一样， 即线程私有；  
- 通过弱引用 来避免内存泄漏


### 4.原理
每个线程都有1个ThreadLocalMap变量, key是ThreadLocal对象, value是Entry对象，其属性只有Object value
```java
# java.lang.Thread
/*
* InheritableThreadLocal values pertaining to this thread. This map is
* maintained by the InheritableThreadLocal class.
*/
ThreadLocal.ThreadLocalMap threadlocal = null
```

而ThreadLocalMap本身是ThreadLocal的静态内部类， 其内部又维护了另一个静态内部类Entry的实例数组

```java

static class ThreadLocalMap {

        /**
         * The entries in this hash map extend WeakReference, using
         * its main ref field as the key (which is always a
         * ThreadLocal object).  Note that null keys (i.e. entry.get()
         * == null) mean that the key is no longer referenced, so the
         * entry can be expunged from table.  Such entries are referred to
         * as "stale entries" in the code that follows.
         */
        static class Entry extends WeakReference<ThreadLocal<?>> {
            /** The value associated with this ThreadLocal. */
            Object value;

            Entry(ThreadLocal<?> k, Object v) {
                super(k);
                value = v;
            }
        }

        /**
         * The initial capacity -- MUST be a power of two.
         */
        private static final int INITIAL_CAPACITY = 16;

        /**
         * The table, resized as necessary.
         * table.length MUST always be a power of two.
         */
        private Entry[] table;
        
        //省略下面的
}
```

通过ThreadLocal.get()时，ThreadLocal转交给
当前线程的ThreadLocalMap去get()
![](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7efe48ec8aa246e1b87d3642f17c4789~tplv-k3u1fbpfcp-watermark.image)

get()的源码如下
```java

 /**
     * Returns the value in the current thread's copy of this
     * thread-local variable.  If the variable has no value for the
     * current thread, it is first initialized to the value returned
     * by an invocation of the {@link #initialValue} method.
     *
     * @return the current thread's value of this thread-local
     */
    public T get() {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null) {
                @SuppressWarnings("unchecked")
                T result = (T)e.value;
                return result;
            }
        }
        return setInitialValue();
    }
```

### 5.为什么使用弱引用WeakReference
目的：防止内存泄漏
### 6.为什么要用hashCode()? hash方法怎么设计的？
- 因为实现Map的时候，使用简单的数组Entry[] 来存储节点，  (而不是TreeMap等方式实现)
	- 如果要根据key来获取Entry 及value，　使用hash比较常见。  

```java
/**
     * The difference between successively generated hash codes - turns
     * implicit sequential thread-local IDs into near-optimally spread
     * multiplicative hash values for power-of-two-sized tables.
     */
    private static final int HASH_INCREMENT = 0x61c88647;

    /**
     * Returns the next hash code.
     */
    private static int nextHashCode() {
        return nextHashCode.getAndAdd(HASH_INCREMENT);
    }
```
上面源码中的magic number，其实是斐波那契数列的魔数，每次hash得到的结果
![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1e5cba37d0fc4ed996810ebb7979024f~tplv-k3u1fbpfcp-watermark.image)

下面就枚举了，size分别为16，32， 64的情况下，每次hash得到的index


> 16：0 7 14 5 12 3 10 1 8 15 6 13 4 11 2 9   

> 32：0 7 14 21 28 3 10 17 24 31 6 13 20 27 2 9 16 23 30 5 12 19 26 1 8 15 22 29 4 11 18 25   

> 64：0 7 14 21 28 35 42 49 56 63 6 13 20 27 34 41 48 55 62 5 12 19 26 33 40 47 54 61 4 11 18 25 32 39 46 53 60 3 10 17 24 31 38 45 52 59 2 9 16 23 30 37 44 51 58 1 8 15 22 29 36 43 50 57 

观察上面的index，我们会发现:  
**使用这样的hash方法，在数组填满前，不会冲突。**

### 7.hash冲突的时候怎么解决？

- 冲突时,采用开放地址法,寻找合适的插入位置。index++往后追加
	- 这种方式在冲突频繁的时候，查询性能就差一些，所以尽量要避免冲突。 使用斐波那契hash算法就是尽量避免冲突



