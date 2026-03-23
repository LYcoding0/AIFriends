from django.contrib import admin

# 先导入模型
from web.models.user import UserProfile
from web.models.character import Character, Voice
from web.models.friend import Friend, Message, SystemPrompt


@admin.register(UserProfile)  # 将UserProfile模型注册到Django管理后台
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)  # 列表页显示字段


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'voice')


admin.site.register(Voice)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('me', 'character',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('friend',)


# 无外键，直接 注册
admin.site.register(SystemPrompt)
