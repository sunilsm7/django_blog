from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.serializers import (
	HyperlinkedModelSerializer,
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField
	)

from posts.models import Post, Comment

# comments serializers
comment_detail_url = HyperlinkedIdentityField(
		view_name='posts-api:comment-detail',
		#lookup_field='id'
		)


class CommentCreateUpdateSerializer(ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
		model = Comment
		fields = ['user', 'post', 'content', 'parent', 'timestamp']
		read_only_fields = ('timestamp', 'user')

	def get_user(self, obj):
		return obj.user.username


class CommentDetailSerializer(ModelSerializer):
	replies = serializers.SerializerMethodField()
	replies_count = serializers.SerializerMethodField()
	url = comment_detail_url
	class Meta:
		model = Comment
		fields = [
			'url',
			'id',
			'user',
			'post',
			'parent',
			'content',
			'updated',
			'timestamp',
			'replies_count',
			'replies'
		]
		read_only_fields = ('post', 'parent',)

	def get_replies(self, obj):
		replies = CommentSerializer(obj.has_replies(), many=True, context=self.context).data
		return replies

	def get_replies_count(self, obj):
		count = obj.has_replies().count()
		return count


class CommentSerializer(ModelSerializer):
	url = comment_detail_url
	replies_count = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()

	class Meta:
		model 	= Comment
		fields 	= [
			'url',
			'id', 
			'user',
			'post',
			'parent',
			'content',
			'updated',
			'timestamp',
			'replies_count'
			]
		read_only_fields = ('id', 'user', 'timestamp', 'replies_count')

	def get_replies_count(self, obj):
		count = obj.has_replies().count()
		return count

	def get_user(self, obj):
		return obj.user.username


# Post Serializers
post_detail_url = HyperlinkedIdentityField(
		view_name='posts-api:post-detail',
		#lookup_field='id'
		)


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = ('title','content','draft','read_time')


class PostDetailSerializer(ModelSerializer):
	comments = serializers.SerializerMethodField()
	html = serializers.SerializerMethodField()
	comment_count = serializers.SerializerMethodField()
	url = post_detail_url
	user = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = [
		'url',
		'id',
		'user',
		'title',
		'slug',
		'content',
		'html',
		'draft',
		'publish',
		'read_time',
		'views',
		'updated',
		'timestamp',
		'comment_count',
		'comments'
		]
	
	def get_comments(self, obj):
		# c_queryset = Comment.objects.filter(post=obj)
		comments = CommentSerializer(obj.get_comments, many=True, context=self.context).data
		return comments	

	def get_comment_count(self, obj):
		count = obj.get_comments.count() # alternatively => count = obj.comments.count()
		return count		

	def get_html(self, obj):
		return obj.get_content_as_markdown()

	def get_user(self, obj):
		return obj.user.username

class PostListSerializer(ModelSerializer):
	comments_count = serializers.SerializerMethodField()
	user = serializers.SerializerMethodField()
	url = post_detail_url
	class Meta:
		model = Post
		fields 	= ('url','title','slug','user','content','publish','read_time','views','comments_count')

	def get_comments_count(self, obj):
		count = obj.get_comments.count()
		return count

	def get_user(self, obj):
		return obj.user.username
		