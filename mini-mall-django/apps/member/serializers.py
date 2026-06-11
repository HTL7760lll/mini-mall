from rest_framework import serializers
from .models import Member, Address


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    name = serializers.CharField(source='nickname', required=True)

    class Meta:
        model = Member
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'email': {'required': True}}

    def validate_email(self, value):
        if Member.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def create(self, validated_data):
        from .models import Member
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = email.split('@')[0]
        base = username; i = 1
        while Member.objects.filter(username=username).exists():
            username = f'{base}{i}'; i += 1

        member = Member.objects.create(username=username, email=email, **validated_data)
        member.set_password(password)
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class MemberInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'email', 'nickname', 'avatar', 'gender', 'phone', 'role', 'status']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'receiver_name', 'receiver_phone', 'province', 'city',
                  'district', 'detail', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        member = self.context['request'].user
        if validated_data.get('is_default'):
            Address.objects.filter(member=member, is_default=True).update(is_default=False)
        return Address.objects.create(member=member, **validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_default'):
            Address.objects.filter(member=instance.member, is_default=True).update(is_default=False)
        return super().update(instance, validated_data)
