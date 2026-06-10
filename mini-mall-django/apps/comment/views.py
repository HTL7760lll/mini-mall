from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def goods_comments(request, goods_id):
    """商品评价列表"""
    comments = Comment.objects.filter(goods_id=goods_id, is_show=True, deleted=False)
    return Response({'code': 200, 'msg': 'success', 'data': CommentSerializer(comments, many=True).data})


@api_view(['POST'])
def comment_save(request):
    """发表评价"""
    data = request.data
    comment = Comment.objects.create(
        goods_id=data['goodsId'],
        order_id=data.get('orderId'),
        member=request.user,
        content=data['content'],
        star=data['star'],
        images=data.get('images', ''),
    )
    return Response({'code': 200, 'msg': '评价成功', 'data': CommentSerializer(comment).data})
