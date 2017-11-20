from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.serializers import (
	HyperlinkedModelSerializer,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )

from posts.models import Post, Comment


class UserSerializer(HyperlinkedModelSerializer):
	posts = serializers.HyperlinkedRelatedField(many=True, queryset=Post.objects.all(), view_name='user-detail')

	class Meta:
		model = User
		fields = ('url', 'username', 'posts')


class PostSerializer(HyperlinkedModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	class Meta:
		model 	= Post
		fields 	= ('url','user','title','slug','content','draft','publish','read_time','views')


class CommentSerializer(HyperlinkedModelSerializer):
	# comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')
	# parent_id = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
	class Meta:
		model 	= Comment
		fields 	= ('id', 'user','content','updated', 'timestamp')