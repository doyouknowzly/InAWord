# nginx使用



## 0. 重启、启动前，校验nginx配置是否语法正确

```shell
./nginx -t
```

t表示测试的意思



### 一、默认目录

```shell
cd /usr/local/nginx/sbin
```



### 二、启动

```shell
./nginx
```



### 三、停止 

```shell
./nginx -s stop
```



### 四、重新加载

```shell
./nginx -s reload
```



### 五、配置文件

```shell
vim /usr/local/nginx/conf/nginx.conf
```

