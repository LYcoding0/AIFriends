from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.friend import Friend
from web.views.friend.message.request_state import get_active_request_cache_key


class InterruptMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        friend_id = request.data.get('friend_id')
        if not friend_id:
            return Response({
                'result': '缺少 friend_id'
            })

        friend = Friend.objects.filter(pk=friend_id, me__user=request.user).first()
        if not friend:
            return Response({
                'result': '对话不存在'
            })

        cache.set(get_active_request_cache_key(friend.id), '', timeout=3600)
        return Response({
            'result': 'success'
        })
