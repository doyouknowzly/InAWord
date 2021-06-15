zk分布式锁



```java
package com.oppo.cdo.message.facade;

public interface DistributeLockFacade {

    public boolean doLockWithOutAutoRelease(String lockPath);

    public boolean releaseLock(String lockPath);
}

```



```java
package com.oppo.cdo.message.core.impl;

import com.ctrip.framework.apollo.ConfigService;
import com.oppo.cdo.message.facade.DistributeLockFacade;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.locks.InterProcessMutex;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.PostConstruct;
import java.util.concurrent.TimeUnit;

public class DistributeLockFacadeImpl implements DistributeLockFacade {

    private static final Logger logger = LoggerFactory.getLogger(DistributeLockFacadeImpl.class);

    CuratorFramework client ;

    @Override
    public boolean doLockWithOutAutoRelease(String lockPath) {
        InterProcessMutex zkLock = new InterProcessMutex(client, lockPath);
        try {
            if (zkLock.acquire(200, TimeUnit.MILLISECONDS)) {
                return true;
            }
        }catch (Exception e){
            logger.error("doLock fail ", e);
        }
        return false;
    }


    @Override
    public boolean releaseLock(String lockPath) {
        InterProcessMutex zkLock = new InterProcessMutex(client, lockPath);
        try {
            zkLock.release();
            return true;
        }catch (Exception e){
            logger.error("releaseLock fail ", e);
        }
        return false;
    }


    @PostConstruct
    public CuratorFramework initZooKeeperClient(){

        String address = ConfigService.getAppConfig().getProperty("lock.zk.address",
                "10.176.72.28:2181,10.176.220.2:2181,10.176.147.77:2181");
        CuratorFramework client = CuratorFrameworkFactory.builder()
                .connectString(address)
                .sessionTimeoutMs(5000)
                .connectionTimeoutMs(5000)
                .retryPolicy(new ExponentialBackoffRetry(100, 2))
                .namespace("com.heytap.iis")
                .build();
        client.start();
        this.client = client;
        return client;

    }
}

```

