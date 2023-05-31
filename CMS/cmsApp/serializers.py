from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
class Userserializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','username','password','email','token')
        extra_kwargs = {'password':{'write_only':True}}

    def get_token(self,obj):
        token,created=Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password =serializers.CharField()

    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username,password=password)
        if not user:
            msg = ('Unable to login with provided credentials.')
            raise serializers.ValidationError(msg,code='authorization')
        token,created = Token.objects.get_or_create(user=user)
        attrs['user'] = user
        attrs['token'] = token
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password','first_name','last_name')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class Postserializer(serializers.ModelSerializer):
    likecount = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title','description','content','created_date','updated_date','owner','is_public','likecount']
        read_only_fields = ['likecount']

    def get_likecount(self,obj):
        return obj.like_set.count()

class Likeserializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','post','user','created_date']

