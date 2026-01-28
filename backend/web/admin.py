from django.contrib import admin

from web.models.user import UserProfile


@admin.register(UserProfile)  # 将UserProfile模型注册到Django管理后台
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)  # 列表页显示字段
