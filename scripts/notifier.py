import requests
import json
import os
import hmac
import hashlib
import base64
import time

def send_bark(key, title, body, group="NetOps"):
    """Send notification to iOS via Bark"""
    url = f"https://api.day.app/{key}/{title}/{body}?group={group}"
    try:
        res = requests.get(url, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def send_dingtalk(webhook_url, content, secret=None):
    """Send notification to DingTalk Robot with optional Sign security"""
    url = webhook_url
    if secret:
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"

    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "NetOps 巡检报告",
            "text": content
        }
    }
    try:
        res = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
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
        res = requests.post(webhook_url, data=json.dumps(data), headers=headers, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage for testing
    print("Notification manager ready.")
