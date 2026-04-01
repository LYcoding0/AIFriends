import os

import requests


def list_voice():
    endpoint = os.getenv('VOICE_URL')
    if not endpoint:
        return {'error': '语音服务地址未配置'}

    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "voice-enrollment",
        "input": {
            "action": "list_voice",
            "page_size": 100,
            "page_index": 0
        }
    }
    try:
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        return response.json()
    except requests.RequestException:
        return {'error': '语音服务请求失败，请稍后重试'}
    except ValueError:
        return {'error': '语音服务返回数据异常'}
