import json
import logging
import secrets
import string

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Voice
from web.views.create.character.voice.custom.create_voice import create_voice


logger = logging.getLogger(__name__)


def safe_json_dumps(payload):
    try:
        text = json.dumps(payload, ensure_ascii=False, default=str)
    except Exception:
        return '<unserializable>'

    if len(text) > 2000:
        return text[:2000] + '...'
    return text


def extract_remote_error_message(payload):
    if not isinstance(payload, dict):
        return None

    for key in ['message', 'detail', 'msg', 'error']:
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    err = payload.get('error')
    if isinstance(err, dict):
        for key in ['message', 'detail', 'msg']:
            val = err.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()

    output = payload.get('output')
    if isinstance(output, dict):
        for key in ['message', 'detail', 'msg', 'error']:
            val = output.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        out_err = output.get('error')
        if isinstance(out_err, dict):
            for key in ['message', 'detail', 'msg']:
                val = out_err.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()

    return None


def extract_voice_id(payload):
    def find_voice_id(obj, depth=0):
        if depth > 6:
            return None
        if isinstance(obj, dict):
            voice_id = obj.get('voice_id')
            if voice_id:
                return voice_id
            for v in obj.values():
                found = find_voice_id(v, depth + 1)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = find_voice_id(item, depth + 1)
                if found:
                    return found
        return None

    voice_id = find_voice_id(payload)
    return str(voice_id) if voice_id else None


class CreateCustomVoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # display name can be Chinese; remote prefix must be alphanumeric
            display_name = (request.data.get('name') or request.data.get('prefix') or '').strip()[:100]
            voice_url = (request.data.get('voice_url') or '').strip()

            if not display_name:
                return Response({'result': '请填写音色名称'})
            if not voice_url:
                return Response({'result': '请填写音频地址'})

            # Remote service constraints: alphanumeric only, length <= 10
            alphabet = string.ascii_lowercase + string.digits

            def to_base36(n: int) -> str:
                chars = string.digits + string.ascii_lowercase
                if n <= 0:
                    return '0'
                out = ''
                while n:
                    n, r = divmod(n, 36)
                    out = chars[r] + out
                return out

            uid_code = to_base36(int(request.user.id))[-4:].rjust(4, '0')
            rand = ''.join(secrets.choice(alphabet) for _ in range(5))
            remote_prefix = f"u{uid_code}{rand}"  # 1 + 4 + 5 = 10

            remote_data = create_voice(voice_url, remote_prefix)
            if isinstance(remote_data, dict) and remote_data.get('error'):
                logger.warning('Create custom voice failed. reason=%s', remote_data.get('error'))
                return Response({'result': remote_data.get('error')})

            remote_voice_id = extract_voice_id(remote_data)
            if not remote_voice_id:
                remote_msg = extract_remote_error_message(remote_data)
                logger.warning(
                    'Voice service response missing voice_id. msg=%s payload=%s',
                    remote_msg or 'unknown',
                    safe_json_dumps(remote_data)
                )
                return Response({'result': remote_msg or '创建远端音色失败，请稍后重试'})

            voice_id_used_by_others = Voice.objects.filter(voice_id=remote_voice_id).exclude(owner=request.user).exists()
            if voice_id_used_by_others:
                return Response({'result': '该音色与其他用户冲突，请重新创建'})

            voice, _ = Voice.objects.update_or_create(
                owner=request.user,
                voice_id=remote_voice_id,
                defaults={
                    'name': display_name,
                    'is_custom': True,
                }
            )

            return Response({
                'result': 'success',
                'voice': {
                    'id': voice.id,
                    'name': voice.name,
                    'is_custom': voice.is_custom,
                    'can_delete': True,
                }
            })
        except Exception:
            logger.exception('CreateCustomVoiceView crashed')
            return Response({'result': '系统异常，请稍后重试'})
