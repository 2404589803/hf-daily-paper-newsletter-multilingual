import logging
import base64
import hashlib
import hmac
import os
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple

def setup_logger():
    """
    设置并配置日志记录器
    Returns:
        logging.Logger: 配置好的日志记录器实例
    """
    # 创建日志记录器
    logger = logging.getLogger('paper_downloader')
    logger.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger 

class APIKeyManager:
    def __init__(self, master_key: str):
        """
        初始化 API Key 管理器
        Args:
            master_key: 主密钥，用于加密和验证
        """
        self.master_key = master_key.encode('utf-8')
        
    def encrypt_api_key(self, api_key: str, valid_hours: int = 24) -> str:
        """
        加密 API key
        Args:
            api_key: 原始 API key
            valid_hours: 有效期（小时）
        Returns:
            加密后的 token
        """
        # 生成过期时间
        expiry = int((datetime.now() + timedelta(hours=valid_hours)).timestamp())
        
        # 生成随机盐值
        salt = os.urandom(16)
        salt_b64 = base64.b64encode(salt).decode('utf-8')
        
        # 组合数据
        data = f"{api_key}:{expiry}:{salt_b64}"
        
        # 计算 HMAC
        signature = hmac.new(
            self.master_key,
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 组合最终 token
        token = f"{data}:{signature}"
        return base64.b64encode(token.encode('utf-8')).decode('utf-8')
    
    def decrypt_api_key(self, encrypted_token: str) -> Optional[str]:
        """
        解密并验证 API key
        Args:
            encrypted_token: 加密的 token
        Returns:
            解密后的 API key，如果验证失败则返回 None
        """
        try:
            # 解码 token
            token = base64.b64decode(encrypted_token.encode('utf-8')).decode('utf-8')
            data, received_signature = token.rsplit(':', 1)
            api_key, expiry_str, _ = data.split(':', 2)
            
            # 验证签名
            expected_signature = hmac.new(
                self.master_key,
                data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, received_signature):
                return None
                
            # 验证是否过期
            expiry = int(expiry_str)
            if time.time() > expiry:
                return None
                
            return api_key
            
        except Exception:
            return None
    
    def verify_api_key(self, encrypted_token: str) -> Tuple[bool, str]:
        """
        验证加密的 API key
        Args:
            encrypted_token: 加密的 token
        Returns:
            (是否有效, 错误信息)
        """
        api_key = self.decrypt_api_key(encrypted_token)
        if api_key is None:
            return False, "Invalid or expired API key"
        return True, "" 