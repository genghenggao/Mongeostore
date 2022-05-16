from rest_framework import serializers
from .models import UploadInfo, UserInfo
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo  # 对应的Model中的类
      
        fields = "__all__"  # 字段，如果是__all__,就是表示列出所有的字段
class UploadInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadInfo
        files = "__all__"