# Lua脚本的使用

[toc]





## 1.LUA脚本的作用

**目的**：通过脚本包含多个redis操作，使得这些指令可以由服务器原子地执行(而不会因为多路复用而中途去处理其他指令)

**用法**:  redis-cli --eval  [lua脚本文件]

1.1 为什么Redis要引入Lua脚本？

​	虽然Redis服务器是单线程的，但使用了多路复用技术， 可能客户端A的连续两条命令A1,A2之间，被客户端B的命令B1插队了，就可能数据不一致，

(即，A1+A2不是原子的)

1.2 使用Lua脚本的好处

1. Redis 服务器会单线程原子性执行 Lua 脚本，保证 Lua 脚本在处理的过程中不会被任意其它请求打断。
2. 减少网络开销。可以将多个请求通过脚本的形式一次发送，减少网络时延
3. 复用。客户端发送的脚本会永久存在redis中，这样其他客户端可以复用这一脚本，而不需要使用代码完成相同的逻辑。

1.3 Lua语言相关

​	Lua是一种轻量小巧的脚本语言，用标准C语言编写并以源代码形式开放。

​	比如：Lua脚本用在很多游戏上(比如魔兽世界)，主要是Lua脚本可以嵌入到其他程序中运行，游戏升级的时候，可以直接升级脚本，而不用重新安装游戏



## 2.常用命令

#### EVAL  ： 执行一段脚本

```lua
EVAL script numkeys key [key …] arg [arg …]
```

#### SCRIPT LOAD  ：将脚本 script 添加到Redis服务器的脚本缓存中。

该命令并不立即执行这个脚本，而是会立即对输入的脚本进行求值。并返回给定脚本的 SHA1 校验和

```lua
SCRIPT LOAD script
```

#### EVALSHA  ： 通过指定sha1校验和，来映射load过的某一段脚本，然后执行它

```lua
EVALSHA sha1 numkeys key [key …] arg [arg …]
```

#### SCRIPT EXISTS ： 校验脚本是否存在

```lua
SCRIPT EXISTS sha1 [sha1 …]
```

#### SCRIPT FLUSH :  清除Redis服务端所有 Lua 脚本缓存

#### SCRIPT KILL :   杀死当前正在运行的 Lua 脚本.

当且仅当这个脚本没有执行过任何写操作时，这个命令才生效。 

这个命令主要用于终止运行时间过长的脚本，比如一个因为 BUG 而发生无限 loop 的脚本.

> 假如当前正在运行的脚本已经执行过写操作，那么即使执行`SCRIPT KILL`，也无法将它杀死，因为这是违反 Lua 脚本的原子性执行原则的。在这种情况下，唯一可行的办法是使用`SHUTDOWN NOSAVE`命令

## 3.Lua脚本的编写

Lua脚本使用redis.call函数或者redis.pcall函数执行一个Redis命令。

> redis.call()与redis.pcall()相似，二者唯一不同之处在于如果执行的redis命令执行失败，redis.call()将产生一个Lua error，从而迫使EVAL命令返回一个错误给命令的调用者，然而redis.pcall()将会捕捉这个错误，并返回代表这个错误的Lua表

比如我们先设置一下key,value

```lua
set zly 25
get zly
> 25
```

再使用lua脚本去get，结果和直接get是一样的

```lua
eval "return redis.call('get','zly')" 0
> 25
```



## 4. 秒杀系统的脚本demo

```lua
local key_local = redis.call('setnx',KEYS[1],0)

if tonumber(key_local) == 0 then
    if tonumber(redis.call('get',KEYS[1]))>=tonumber(ARGV[2]) then
        return false
    else
        redis.call('incr',KEYS[1])
        return true
    end
else
    redis.call('incr',KEYS[1])
    redis.call('pexpire',KEYS[1],ARGV[1])
    return true
end
```



JAVA客户端

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.scripting.support.ResourceScriptSource;
import org.springframework.stereotype.Component;

import java.util.Collections;

@Component
public class GlobalLimitComponent {
    @Autowired
    private StringRedisTemplate redisTemplate;

    /**
     * 针对某个key使用lua脚本进行限流
     * 使用lua优点，可以保证多个命令是一次行传输到Redis服务器并且是串行执行的，保证串行执行的命令中不行插入其他命令，防止并发问题
     * 步骤：
     * 1、判断key是否存在，如果不存在，保存该key，设置值为1，设置多少毫秒（n）最多进行几次（m)
     * 2、如果值存在，先判断key是否超时了，如果超时则删除，并重新执行步骤1，如果key未超时，则判断是否超过n毫秒最多m次的限制
     *
     * @param key
     */
    public Boolean getGlobalLimitByLua(String key, int mlitimes, int maxCount) {
        DefaultRedisScript<Boolean> redisScript = new DefaultRedisScript<>();
        redisScript.setScriptSource(new ResourceScriptSource(new ClassPathResource("/limit.lua")));
        redisScript.setResultType(Boolean.class);

        return redisTemplate.execute(redisScript, Collections.singletonList(key), String.valueOf(mlitimes), String.valueOf(maxCount));
    }
}
```





## 5. 控制ip访问频率的demo

需求：实现一个访问频率控制，某个IP在短时间内频繁访问页面，需要记录并检测出来，就可以通过Lua脚本高效的实现。

小声说明：本实例针对固定窗口的访问频率，而动态的非滑动窗口。

即：如果规定一分钟内访问10次，记为超限。在本实例中前一分钟的最后一秒访问9次，下一分钟的第1秒又访问9次，不计为超限。 

脚本如下 : 

```lua
local visitNum = redis.call('incr', KEYS[1])

if visitNum == 1 then
        redis.call('expire', KEYS[1], ARGV[1])
end

if visitNum > tonumber(ARGV[2]) then
        return 0
end

return 1;
```



## 6.Lua组件

#### 伪客户端：

因为执行Redis命令必须有相应的客户端状态，所以为了执行Lua脚本中包含的Redis命令，Redis服务器专门为Lua环境创建了一个伪客户端，并由这个伪客户端负责处理Lua脚本中包含的所有Redis命令。

Lua脚本使用redis.call函数或者redis.pcall函数执行一个Redis命令，需要完成以下步骤：

1. Lua环境将redis.call函数或者redis.pcall函数想要执行的命令传给伪客户端。
2. 伪客户端将脚本想要执行的命令传给命令执行器。
3. 命令执行器执行伪客户端传给它的命令，并将命令的执行结果返回给伪客户端。
4. 伪客户端接收命令执行器返回的命令结果，并将这个命令结果返回给Lua环境。
5. Lua环境在接收到命令结果之后，将该结果返回给redis.call函数或者redis.pcall函数。
6. 接收到结果的redis.call函数或者redis.pcall函数会将命令结果作为函数返回值返回给脚本中的调用者。



#### lua_scripts字典:

有两个作用，一个是**实现SCRIPT EXISTS命令**，另一个是实现**脚本复制**功能

脚本复制，指的是，当服务器运行在复制模式之下时，具有写性质的脚本命令也会被复制到从服务器，

这些命令包括EVAL命令、EVALSHA命令、SCRIPT FLUSH命令，以及SCRIPT LOAD命令

