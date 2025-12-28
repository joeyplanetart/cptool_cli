"""钉钉通知模块"""
import aiohttp
import asyncio
from typing import Optional


async def send_dingding_notification(
    webhook_url: str,
    title: str,
    content: str,
    msg_type: str = "markdown"
):
    """发送钉钉通知
    
    Args:
        webhook_url: 钉钉机器人Webhook URL
        title: 消息标题
        content: 消息内容
        msg_type: 消息类型（text或markdown）
    """
    if not webhook_url:
        return
    
    try:
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


def send_dingding_sync(webhook_url: str, title: str, content: str):
    """同步发送钉钉通知（封装异步调用）"""
    if webhook_url:
        asyncio.run(send_dingding_notification(webhook_url, title, content))

