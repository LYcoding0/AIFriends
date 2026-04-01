from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Voice


class ListCustomVoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            voices_raw = Voice.objects.filter(owner=request.user, is_custom=True).order_by('id')
            voices = []
            for v in voices_raw:
                voices.append({
                    'id': v.id,
                    'name': v.name,
                    'is_custom': True,
                    'can_delete': True,
                })

            return Response({
                'result': 'success',
                'voices': voices,
            })
        except Exception:
            return Response({'result': '系统异常，请稍后重试'})
