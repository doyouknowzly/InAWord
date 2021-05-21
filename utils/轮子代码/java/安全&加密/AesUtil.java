package com.oppo.cdo.pay.common.safety;

import com.oppo.framework.common.util.AESUtils;
import org.apache.commons.codec.binary.Hex;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.UUID;

public final class AesUtil {
    
    private static final Logger logger = LoggerFactory.getLogger(AesUtil.class);
    
    private AesUtil() {}
    

    
    public static String encrypt(String key, String text) throws Exception {
        Cipher cipher = Cipher.getInstance("AES/CBC/NOPadding");
        int blockSize = cipher.getBlockSize();
        byte[] dataBytes = text.getBytes(StandardCharsets.UTF_8);
        int plaintextLen = dataBytes.length;
        if (plaintextLen % blockSize != 0) {
            plaintextLen = plaintextLen + (blockSize - plaintextLen % blockSize);
        }
        byte[] plaintext = new byte[plaintextLen];
        System.arraycopy(dataBytes, 0, plaintext, 0, dataBytes.length);
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(key.getBytes(StandardCharsets.UTF_8));
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, ivSpec);
        byte[] encryptBytes = cipher.doFinal(plaintext);
        return Base64.getEncoder().encodeToString(encryptBytes);
    }
    
    public static String decrypt(String key, String cipherText) throws Exception {
        byte[] baseDecryptBytes = Base64.getDecoder().decode(cipherText);
        Cipher cipher = Cipher.getInstance("AES/CBC/NOPadding");
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "AES");
        IvParameterSpec ivSpec = new IvParameterSpec(key.getBytes(StandardCharsets.UTF_8));
        cipher.init(Cipher.DECRYPT_MODE, keySpec, ivSpec);
        byte[] org = cipher.doFinal(baseDecryptBytes);
        return new String(org, StandardCharsets.UTF_8).trim();
    }
    
    public static void generateSecret() {
        try {
            String random = UUID.randomUUID().toString().replaceAll("-", "");
            System.out.println("random=" + random);
            KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
            keyGenerator.init(new SecureRandom(random.getBytes()));
            SecretKey secretKey = keyGenerator.generateKey();
            byte[] contentBytes = secretKey.getEncoded();
            System.out.println(contentBytes.length);
            System.out.println(Hex.encodeHexString(contentBytes));
            System.out.println(Hex.encodeHexString(contentBytes).substring(0, 16));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws Exception{
        generateSecret();
        String key1 = "acb8da286df6b665";

        String plainText = "zly test";
        System.out.println("plain_text: " + plainText);
        String cipher = encrypt(key1, plainText);
        System.out.println("cipher : " + cipher);
        String afterDesc = decrypt(key1, cipher);
        System.out.println("afterDesc: " + afterDesc);

    }
}
