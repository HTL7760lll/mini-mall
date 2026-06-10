from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image_url', 'link_url', 'link_type', 'link_target', 'sort', 'status', 'created_at']
