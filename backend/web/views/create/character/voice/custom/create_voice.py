import os
import logging

import requests


logger = logging.getLogger(__name__)


def extract_remote_error_message(payload):
    if not isinstance(payload, dict):
        return None

    direct_candidates = [
        payload.get('message'),
        payload.get('detail'),
        payload.get('msg'),
    ]
    for msg in direct_candidates:
        if isinstance(msg, str) and msg.strip():
            return msg.strip()

    err = payload.get('error')
    if isinstance(err, str) and err.strip():
        return err.strip()
    if isinstance(err, dict):
        for key in ['message', 'detail', 'msg']:
            val = err.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

    output = payload.get('output')
    if isinstance(output, dict):
        for key in ['message', 'detail', 'msg']:
            val = output.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        out_err = output.get('error')
        if isinstance(out_err, str) and out_err.strip():
            return out_err.strip()
        if isinstance(out_err, dict):
            for key in ['message', 'detail', 'msg']:
                val = out_err.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()

    return None


def create_voice(voice_url, prefix):
    endpoint = os.getenv('VOICE_URL')
    if not endpoint:
        return {'error': '语音服务地址未配置'}

    api_key = os.getenv('API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "voice-enrollment",
        "input": {
            "action": "create_voice",
            "target_model": "cosyvoice-v3-flash",
            "prefix": prefix,
            "url": voice_url,
        }
    }
    try:
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        try:
            payload = response.json()
        except ValueError:
            logger.warning(
                'Voice service returned non-JSON response. status=%s content_type=%s',
                response.status_code,
                response.headers.get('Content-Type')
            )
            return {'error': '语音服务返回数据异常'}

        if isinstance(payload, dict):
            payload.setdefault('_http_status', response.status_code)

        if response.status_code >= 400:
            remote_msg = extract_remote_error_message(payload)
            logger.warning('Voice service error. status=%s msg=%s', response.status_code, remote_msg or 'unknown')
            return {'error': remote_msg or f'语音服务请求失败({response.status_code})'}

        return payload
    except requests.RequestException:
        return {'error': '语音服务请求失败，请稍后重试'}
    except ValueError:
        return {'error': '语音服务返回数据异常'}
