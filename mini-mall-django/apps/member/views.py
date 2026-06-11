from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Member, Address
from .serializers import (
    RegisterSerializer, LoginSerializer,
    MemberInfoSerializer, AddressSerializer
)


class LoginRateThrottle(AnonRateThrottle):
    rate = '5/min'  # 登录严格限流


class RegisterRateThrottle(AnonRateThrottle):
    rate = '3/min'  # 注册更严格


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
        'refresh': str(refresh),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([RegisterRateThrottle])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)
    user = serializer.save()
    tokens = get_tokens_for_user(user)
    return Response({
        'code': 200, 'msg': '注册成功',
        'data': {
            'token': tokens['token'],
            'userId': user.id,
            'email': user.email,
            'nickname': user.nickname,
            'role': user.role,
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    # 用 email 查找用户
    try:
        user = Member.objects.get(email=email)
        if not user.check_password(password):
            return Response({'code': 1002, 'msg': '邮箱或密码错误'}, status=400)
    except Member.DoesNotExist:
        return Response({'code': 1002, 'msg': '邮箱或密码错误'}, status=400)

    if user.status == 0:
        return Response({'code': 1004, 'msg': '账号已被禁用'}, status=400)

    tokens = get_tokens_for_user(user)
    return Response({
        'code': 200, 'msg': '登录成功',
        'data': {
            'token': tokens['token'],
            'userId': user.id,
            'email': user.email,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'role': user.role,
        }
    })


@api_view(['GET', 'PUT'])
def profile(request):
    if request.method == 'GET':
        return Response({
            'code': 200, 'msg': 'success',
            'data': MemberInfoSerializer(request.user).data
        })
    if request.method == 'PUT':
        user = request.user
        data = request.data
        for field in ['nickname', 'avatar', 'gender', 'phone']:
            if field in data:
                setattr(user, field, data[field])
        user.save()
        return Response({'code': 200, 'msg': '修改成功'})


# ====== Address Views ======

@api_view(['GET', 'POST'])
def address_list(request):
    if request.method == 'GET':
        addresses = Address.objects.filter(member=request.user, deleted=False)
        serializer = AddressSerializer(addresses, many=True)
        return Response({'code': 200, 'msg': 'success', 'data': serializer.data})

    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'msg': '保存成功', 'data': serializer.data})
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def address_detail(request, pk):
    try:
        address = Address.objects.get(pk=pk, member=request.user, deleted=False)
    except Address.DoesNotExist:
        return Response({'code': 4001, 'msg': '地址不存在'}, status=404)

    if request.method == 'GET':
        return Response({'code': 200, 'msg': 'success', 'data': AddressSerializer(address).data})

    if request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 200, 'msg': '修改成功'})
        return Response({'code': 400, 'msg': str(serializer.errors)}, status=400)

    if request.method == 'DELETE':
        address.deleted = True
        address.save()
        return Response({'code': 200, 'msg': '删除成功'})


@api_view(['PUT'])
def address_set_default(request, pk):
    try:
        address = Address.objects.get(pk=pk, member=request.user, deleted=False)
    except Address.DoesNotExist:
        return Response({'code': 4001, 'msg': '地址不存在'}, status=404)
    Address.objects.filter(member=request.user, is_default=True).update(is_default=False)
    address.is_default = True
    address.save()
    return Response({'code': 200, 'msg': '设置成功'})
