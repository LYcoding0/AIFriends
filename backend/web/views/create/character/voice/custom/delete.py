from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character, Voice
from web.views.create.character.voice.custom.delete_voice import delete_voice


class DeleteCustomVoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            voice_id = request.data.get('voice_id')
            if not voice_id:
                return Response({'result': '音色不存在'})

            voice = Voice.objects.filter(id=voice_id, owner=request.user, is_custom=True).first()
            if not voice:
                return Response({'result': '音色不存在或无权限'})

            in_use = Character.objects.filter(voice=voice).exists()
            if in_use:
                return Response({'result': '该音色正在被角色使用，请先更换后再删除'})

            same_remote_voice_exists = Voice.objects.filter(voice_id=voice.voice_id).exclude(id=voice.id).exists()
            if not same_remote_voice_exists:
                remote_data = delete_voice(voice.voice_id)
                if isinstance(remote_data, dict) and remote_data.get('error'):
                    return Response({'result': remote_data.get('error')})

            voice.delete()

            return Response({'result': 'success'})
        except Exception:
            return Response({'result': '系统异常，请稍后重试'})
