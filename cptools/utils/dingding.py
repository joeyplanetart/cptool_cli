"""钉钉通知模块"""
import aiohttp
import asyncio
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus
from typing import Optional


def generate_sign(secret: str) -> tuple:
    """生成钉钉签名
    
    Args:
        secret: 钉钉机器人的密钥
        
    Returns:
        (timestamp, sign) 时间戳和签名
    """
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(
        secret_enc,
        string_to_sign_enc,
        digestmod=hashlib.sha256
    ).digest()
    sign = quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


async def send_dingding_notification(
    webhook_url: str,
    title: str,
    content: str,
    secret: Optional[str] = None,
    msg_type: str = "markdown"
):
    """发送钉钉通知
    
    Args:
        webhook_url: 钉钉机器人Webhook URL
        title: 消息标题
        content: 消息内容
        secret: 钉钉机器人签名密钥（可选）
        msg_type: 消息类型（text或markdown）
    """
    if not webhook_url:
        return
    
    try:
        # 如果提供了签名密钥，生成签名并添加到URL
        if secret:
            timestamp, sign = generate_sign(secret)
            if '?' in webhook_url:
                webhook_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"
            else:
                webhook_url = f"{webhook_url}?timestamp={timestamp}&sign={sign}"
        
        if msg_type == "markdown":
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content
                }
            }
        else:
            data = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=data) as resp:
                result = await resp.json()
                if result.get("errcode") != 0:
                    print(f"钉钉通知发送失败: {result.get('errmsg')}")
                else:
                    print("钉钉通知发送成功")
    except Exception as e:
        print(f"发送钉钉通知时出错: {str(e)}")

