## jmap

**jmap -dump:live,format=b,file=dump.hprof PID**

生成内存快照，以供分析内存占用情况。



**jhat dump.hprof**

分析内存快照，内置了web容器，可以通过浏览器分析堆内存快照。