https://www.jianshu.com/p/ab7cf5484e8f

# 使用方式

将server节点下的location节点中的proxy_pass配置为：http:// + upstream名称，即“
 http://xxx_server_name”
 示例:



```nginx
location / { 
    root  html; 
    index  index.html index.htm; 
    proxy_pass http://xxx_server_name; 
}
```

