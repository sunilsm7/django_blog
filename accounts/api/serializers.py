from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.serializers import (
	HyperlinkedModelSerializer,
	HyperlinkedIdentityField,
	ModelSerializer,
	Serializer,
	SerializerMethodField
	)

from rest_framework.validators import UniqueValidator
from posts.api.serializers import PostListSerializer, CommentSerializer
from posts.models import Post, Comment

user_detail_url = HyperlinkedIdentityField(
		view_name='users-api:user-detail',
		#lookup_field='id'
		)

class UserDetailSerializer(ModelSerializer):
	url = user_detail_url
	posts = serializers.SerializerMethodField()
	posts_count = serializers.SerializerMethodField()
	comments_count = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('url', 'username','first_name', 'last_name','posts_count','comments_count','posts')

	def get_posts(self, obj):
		queryset = Post.objects.filter(user=obj)
		posts = PostListSerializer(queryset, many=True, context=self.context).data
		return posts

	def get_posts_count(self, obj):
		count = obj.posts.count()
		return count

	def get_comments_count(self, obj):
		queryset = Comment.objects.filter(user=obj).count()
		return queryset


class UserSerializer(ModelSerializer):
	url = user_detail_url
	posts_count = serializers.SerializerMethodField()
	comments_count = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('url','id', 'username', 'groups','posts_count','comments_count')
		read_only_fields = ('id',)

	def get_posts_count(self, obj):
		count = obj.posts.count()
		return count

	def get_comments_count(self, obj):
		queryset = Comment.objects.filter(user=obj).count()
		#comments = CommentSerializer(user=obj, many=True, context=self.context).data
		return queryset


class SignUpSerializer(ModelSerializer):
	email = serializers.EmailField(
		max_length=120,
		validators =[UniqueValidator(
			queryset = User.objects.all(),
			message = 'email id already used.',
			lookup='iexact'
			)]
		)

	class Meta:
		model = User
		fields = ('id','username', 'email', 'password')
		read_only_fields = ('id',)
		

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']

		if len(password) < 8:
			raise serializers.ValidationError("Password must be at least 8 characters")
		user_obj = User(
				username = username,
				email = email
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data


class LoginSerializer(ModelSerializer):
	token = serializers.CharField(allow_blank=True, read_only=True)
	username = serializers.CharField()

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'token',
			
		]
		extra_kwargs = {"password":
							{"write_only": True}
							}

	def validate(self, data):
		username = data['username']
		qs = User.objects.filter(username=username) 
		if qs.exists():
			user = qs.first()
			email = user.email
			token, _ = Token.objects.get_or_create(user=user)
			data = {
				'username':username,
				'token':token,
				'email':email,
			}
		return data


class AuthTokenSerializer(serializers.Serializer):
	username = serializers.CharField(label=_("Username"))
	password = serializers.CharField(
		label=_("Password"),
		style={'input_type': 'password'},
		trim_whitespace=False
	)

	def validate(self, attrs):
		username = attrs.get('username')
		password = attrs.get('password')

		if username and password:
			user = authenticate(request=self.context.get('request'),
								username=username, password=password)
			if user:
				if not user.is_active:
					msg = _('User account is disabled.')
					raise serializers.ValidationError(msg, code='authorization')
			else:
				msg = _('Unable to log in with provided credentials.')
				raise serializers.ValidationError(msg, code='authorization')
		else:
			msg = _('Must include "username" and "password".')
			raise serializers.ValidationError(msg, code='authorization')

		attrs['user'] = user
		return attrs