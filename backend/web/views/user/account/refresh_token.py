from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from backend import settings


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({
                    'result': 'refresh token 不存在'
                }, status=401)
            refresh = RefreshToken(refresh_token)  # 生成refresh_token,如果过期异常,触发except
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                refresh.set_jti()  # 刷新refresh_token
                response = Response({  # 返回前端是access，返回cookie是refresh
                    'result': 'success',
                    'access': str(refresh.access_token),
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
                'result': 'success',
                'access': str(refresh.access_token),
            })
        except:
            return Response({
                'result': 'refresh token 过期了'
            }, status=401)
