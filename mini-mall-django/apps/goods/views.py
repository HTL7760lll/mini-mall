from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import GoodsCategory, Goods
from .serializers import CategorySerializer, GoodsListSerializer, GoodsDetailSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def category_tree(request):
    """商品分类树"""
    roots = GoodsCategory.objects.filter(parent__isnull=True, status=1, deleted=False) \
        .annotate(goods_count=Count('goods', filter=Q(goods__status=1, goods__deleted=False))) \
        .prefetch_related('children').order_by('sort')
    return Response({'code': 200, 'msg': 'success', 'data': CategorySerializer(roots, many=True).data})


class GoodsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'pageSize'
    page_query_param = 'page'


@api_view(['GET'])
@permission_classes([AllowAny])
def goods_list(request):
    """商品分页列表 (支持分类筛选+排序+搜索)"""
    queryset = Goods.objects.filter(status=1, deleted=False)

    category_id = request.query_params.get('categoryId')
    if category_id:
        # 支持子分类: 匹配当前分类及其子分类
        sub_ids = list(GoodsCategory.objects.filter(parent_id=category_id, status=1, deleted=False)
                       .values_list('id', flat=True))
        sub_ids.append(int(category_id))
        queryset = queryset.filter(category_id__in=sub_ids)

    keyword = request.query_params.get('keyword')
    if keyword:
        queryset = queryset.filter(name__icontains=keyword)

    # 价格区间
    min_price = request.query_params.get('minPrice')
    max_price = request.query_params.get('maxPrice')
    if min_price:
        queryset = queryset.filter(price__gte=float(min_price))
    if max_price:
        queryset = queryset.filter(price__lte=float(max_price))
    if keyword:
        queryset = queryset.filter(name__icontains=keyword)

    sort = request.query_params.get('sort', '')
    if sort == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort == 'sales':
        queryset = queryset.order_by('-sales')
    else:
        queryset = queryset.order_by('sort', '-created_at')

    paginator = GoodsPagination()
    page = paginator.paginate_queryset(queryset, request)
    serializer = GoodsListSerializer(page, many=True)

    return Response({
        'code': 200, 'msg': 'success',
        'data': {
            'total': paginator.page.paginator.count,
            'pages': paginator.page.paginator.num_pages,
            'current': paginator.page.number,
            'size': paginator.page_size,
            'records': serializer.data,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def goods_detail(request, pk):
    """商品详情"""
    try:
        goods = Goods.objects.select_related('category').prefetch_related('skus').get(
            pk=pk, status=1, deleted=False)
    except Goods.DoesNotExist:
        return Response({'code': 2001, 'msg': '商品不存在'}, status=404)

    return Response({'code': 200, 'msg': 'success', 'data': GoodsDetailSerializer(goods).data})


@api_view(['GET'])
@permission_classes([AllowAny])
def goods_hot(request):
    """热卖推荐"""
    goods = Goods.objects.filter(status=1, is_hot=True, deleted=False).order_by('-sales')[:10]
    return Response({'code': 200, 'msg': 'success', 'data': GoodsListSerializer(goods, many=True).data})


@api_view(['GET'])
@permission_classes([AllowAny])
def goods_new(request):
    """新品推荐"""
    goods = Goods.objects.filter(status=1, is_new=True, deleted=False).order_by('-created_at')[:10]
    return Response({'code': 200, 'msg': 'success', 'data': GoodsListSerializer(goods, many=True).data})


# ====== 搜索接口 ======

@api_view(['GET'])
@permission_classes([AllowAny])
def goods_search(request):
    """商品搜索 — 独立于 goods_list"""
    keyword = request.query_params.get('keyword', '')
    queryset = Goods.objects.filter(status=1, deleted=False, name__icontains=keyword)

    paginator = GoodsPagination()
    page = paginator.paginate_queryset(queryset.order_by('-sales'), request)
    serializer = GoodsListSerializer(page, many=True)

    return Response({
        'code': 200, 'msg': 'success',
        'data': {
            'total': paginator.page.paginator.count,
            'pages': paginator.page.paginator.num_pages,
            'current': paginator.page.number,
            'size': paginator.page_size,
            'records': serializer.data,
        }
    })
