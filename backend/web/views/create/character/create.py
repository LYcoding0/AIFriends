from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character, Voice
from web.models.user import UserProfile


class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            name = request.data.get('name').strip()
            voice_id = request.data.get('voice_id')
            profile = request.data.get('profile').strip()[:100000]
            photo = request.FILES.get('photo', None)
            background_image = request.FILES.get('background_image', None)

            if not name:
                return Response({
                    'result': '请填写角色名称'
                })
            if not profile:
                return Response({
                    'result': '请填写角色简介'
                })
            if not photo:
                return Response({
                    'result': '请上传角色头像'
                })
            if not background_image:
                return Response({
                    'result': '请上传角色背景图片'
                })

            voice = Voice.objects.filter(
                id=voice_id
            ).filter(
                Q(owner=request.user) | Q(owner__isnull=True)
            ).first()
            if not voice:
                return Response({
                    'result': '音色不存在或无权限'
                })

            Character.objects.create(
                author=user_profile,
                name=name,
                voice=voice,
                profile=profile,
                photo=photo,
                background_image=background_image
            )
            return Response({
                'result': 'success'
            })
        except Exception:
            return Response({
                'result': '系统异常，请稍后重试'
            })
