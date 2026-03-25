from django.core.cache import cache
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.friend import Friend, Message
from web.views.friend.message.request_state import get_active_request_cache_key


class ClearHistoryView(APIView):
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

        deleted_count = Message.objects.filter(friend=friend).count()
        cache.set(get_active_request_cache_key(friend.id), '', timeout=3600)
        Message.objects.filter(friend=friend).delete()
        friend.memory = ''
        friend.update_time = now()
        friend.save(update_fields=['memory', 'update_time'])

        return Response({
            'result': 'success',
            'deleted_count': deleted_count,
        })
