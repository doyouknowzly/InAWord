# emoji相关知识

https://www.jianshu.com/p/8d675a5b9e5c

https://www.jianshu.com/p/32a95a4fc542





## 一、方案1， 修改mysql数据库编码

https://www.cnblogs.com/shihaiming/p/5855616.html

https://www.cnblogs.com/lyc88/articles/13268445.html

## 二、方案2，字符encode一下再存储，读的时候decode一下




```java

package com.heytap.global.community.core.util;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializerFeature;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class EmojiUtil {
    private static final Logger logger = LoggerFactory.getLogger(EmojiUtil.class);
    private static final Pattern EMOJI_PATTERN = Pattern.compile("\\\\u[de][0-9a-f]{3}");

    public static String encode(String content) {
        if (StringUtils.isEmpty(content)) {
            return content;
        }
        try {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < content.length(); i++) {
                char c = content.charAt(i);
                if (c >= 53248 && c <= 61439) {
                    String str = JSON.toJSONString(String.valueOf(c), SerializerFeature.BrowserCompatible).toLowerCase();
                    str = str.replaceAll("\"", "");
                    sb.append(str);
                } else {
                    sb.append(c);
                }
            }
            String result = sb.toString();
            logger.debug("encodeEmoji, req:{},result:{}", content, result);
            return result;
        } catch (Exception e) {
            logger.error("emoji encode 出错, content:{}", content, e);
            return content;
        }
    }



    public static String decode(String content) {
        if (StringUtils.isEmpty(content)) {
            return content;
        }

        try {
            Matcher matcher = EMOJI_PATTERN.matcher(content);
            StringBuffer sb = new StringBuffer();

            while (matcher.find()) {
                String p = matcher.group();
                matcher.appendReplacement(sb, (String) JSON.parse("\"" + p + "\""));
            }
            matcher.appendTail(sb);

            String result = sb.toString();
            logger.debug("decodeEmoji, req:{},result:{}", content, result);
            return result;
        } catch (Exception e) {
            logger.error("emoji decode 出错, content:{}", content, e);
            return content;
        }
    }

}


```

