from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'goods_id', 'order_id', 'member_id', 'member_name',
                  'content', 'star', 'images', 'is_show', 'created_at']

    def get_member_name(self, obj):
        return obj.member.nickname or obj.member.username
