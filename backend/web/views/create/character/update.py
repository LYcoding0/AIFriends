from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character
from web.views.utils.photo import remove_old_photo


class UpdateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            character_id = request.data['character_id']
            # character_id字符串类型会自动转为int类型，__user是UserProfile的属性
            character = Character.objects.get(id=character_id, author__user=request.user)
            name = request.data['name'].strip()
            profile = request.data['profile'].strip()
            photo = request.FILES.get('photo', None)
            background_image = request.FILES.get('background_image', None)

            if not name:
                return Response({
                    'result': '请输入名称'
                })
            if not profile:
                return Response({
                    'result': '请输入简介'
                })

            if photo:
                remove_old_photo(character.photo)
                character.photo = photo

            if background_image:
                remove_old_photo(character.background_image)
                character.background_image = background_image

            character.name = name
            character.profile = profile
            character.updated_time = now()

            character.save()
            return Response({
                'result': 'success'
            })

        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })
