from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username').strip()  # data是字典，是post的参数
            password = request.data.get('password').strip()
            if not username or not password:
                return Response({
                    'result': '用户名或密码不能为空'
                })
            user = authenticate(username=username, password=password)  # 验证用户提供的用户名和密码是否匹配
            if user:  # 不为空，用户名密码匹配
                user_profile = UserProfile.objects.get(user=user)
                refresh = RefreshToken.for_user(user)  # 生成refresh_token
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
                })
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            return Response({
                'result': '用户名或密码错误'
            })
        except:
            import traceback
            print(traceback.format_exc())  # 输出错误信息
            return Response({
                'result': '系统异常，请稍后重试'
            })
