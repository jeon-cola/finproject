# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'nickname', 'age', 'asset', 'salary','saving','deposit']
 
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            age=validated_data.get('age'),
            asset=validated_data.get('asset'),
            salary=validated_data.get('salary'),
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.age = validated_data.get('age', instance.age)
        instance.asset = validated_data.get('asset', instance.asset)
        instance.salary = validated_data.get('salary', instance.salary)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
