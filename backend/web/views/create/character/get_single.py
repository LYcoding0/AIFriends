from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character, Voice


class GetSingleCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            character_id = request.query_params.get('character_id')
            character = Character.objects.filter(id=character_id, author__user=request.user).first()
            if not character:
                return Response({
                    'result': '角色不存在或无权限'
                })

            voices_raw = Voice.objects.filter(
                Q(owner=request.user) | Q(owner__isnull=True)
            ).order_by('id')
            voices = []
            for v in voices_raw:
                voices.append({
                    'id': v.id,
                    'name': v.name,
                    'is_custom': v.is_custom,
                    'can_delete': v.is_custom and v.owner_id == request.user.id,
                })

            return Response({
                'result': 'success',
                'character': {
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'voice_id': character.voice.id if character.voice else None,
                },
                'voices': voices,
            })
        except Exception:
            return Response({
                'result': '系统异常，请稍后重试'
            })
