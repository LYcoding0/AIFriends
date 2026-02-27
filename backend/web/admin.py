from django.contrib import admin

# 先导入模型
from web.models.user import UserProfile
from web.models.character import Character
from web.models.friend import Friend


@admin.register(UserProfile)  # 将UserProfile模型注册到Django管理后台
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)  # 列表页显示字段


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('me', 'character',)
