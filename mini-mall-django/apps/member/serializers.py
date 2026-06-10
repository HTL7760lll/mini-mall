from rest_framework import serializers
from .models import Member, Address


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)

    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'nickname', 'phone']
        extra_kwargs = {'nickname': {'required': False}, 'phone': {'required': False}}

    def validate_username(self, value):
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        nickname = validated_data.pop('nickname', None) or validated_data['username']
        member = Member.objects.create(**validated_data)
        member.nickname = nickname
        member.set_password(password)
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class MemberInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'nickname', 'avatar', 'gender', 'phone', 'role', 'status']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'receiver_name', 'receiver_phone', 'province', 'city',
                  'district', 'detail', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        member = self.context['request'].user
        # 如果设为默认，先取消其他默认
        if validated_data.get('is_default'):
            Address.objects.filter(member=member, is_default=True).update(is_default=False)
        return Address.objects.create(member=member, **validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_default'):
            Address.objects.filter(member=instance.member, is_default=True).update(is_default=False)
        return super().update(instance, validated_data)
