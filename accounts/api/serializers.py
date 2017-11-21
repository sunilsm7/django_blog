from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.serializers import (
	HyperlinkedModelSerializer,
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField
	)
from rest_framework.validators import UniqueValidator
from posts.api.serializers import PostListSerializer
from posts.models import Post, Comment

user_detail_url = HyperlinkedIdentityField(
		view_name='users-api:user-detail',
		#lookup_field='id'
		)

class UserDetailSerializer(ModelSerializer):
	url = user_detail_url
	posts = serializers.SerializerMethodField()
	posts_count = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('url', 'username','first_name', 'last_name','posts_count','posts')

	def get_posts(self, obj):
		queryset = Post.objects.filter(user=obj)
		posts = PostListSerializer(queryset, many=True, context=self.context).data
		return posts

	def get_posts_count(self, obj):
		count = obj.posts.count()
		return count


class UserCreateSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ('id','username', 'email', 'password')
		read_only_fields = ('id',)

	def validate(self, data):
		email = data['email']
		if email == '':
			raise serializers.ValidationError("email id required.")
		else:
			user = User.objects.get(email=email)
			if user is not None: 
				raise serializers.ValidationError("email id already exists.")
		return data

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		return user


class UserSerializer(ModelSerializer):
	url = user_detail_url
	posts_count = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('url','id', 'username', 'posts_count')
		read_only_fields = ('id',)

	def get_posts_count(self, obj):
		count = obj.posts.count()
		return count