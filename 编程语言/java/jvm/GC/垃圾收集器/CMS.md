## CMS



Concurrent - Mark - Sweep , 从名字中就可以看出， CMS采用的是 **标记-清除** 算法



### 一、步骤

1. 初始标记（CMS initial mark）
2. 并发标记（CMS concurrent mark）
3. 重新标记（CMS remark）
4. 并发清除（CMS concurrent sweep）

其中，1初始标记 和 3重新标记会STW



### 二、