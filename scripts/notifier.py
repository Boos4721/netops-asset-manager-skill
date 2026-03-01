import requests
import json
import os

def send_bark(key, title, body, group="NetOps"):
    """Send notification to iOS via Bark"""
    url = f"https://api.day.app/{key}/{title}/{body}?group={group}"
    try:
        res = requests.get(url)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def send_dingtalk(webhook_url, secret, content):
    """Send notification to DingTalk Robot"""
    # Simple text implementation, can be expanded to HMAC sign for security
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "NetOps巡检报告",
            "text": content
        }
    }
    try:
        res = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def send_feishu(webhook_url, content):
    """Send notification to Feishu Robot"""
    headers = {'Content-Type': 'application/json'}
    data = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "NetOps 自动化巡检"}},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": content}}]
        }
    }
    try:
        res = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage for testing
    print("Notification manager ready.")
