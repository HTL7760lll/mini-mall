from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Banner
from .serializers import BannerSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def banner_list(request):
    """获取启用Banner列表"""
    banners = Banner.objects.filter(status=1, deleted=False).order_by('sort')
    return Response({'code': 200, 'msg': 'success', 'data': BannerSerializer(banners, many=True).data})
