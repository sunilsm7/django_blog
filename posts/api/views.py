import datetime
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse

from posts.models import Post, Comment
from .serializers import (
	CommentSerializer,
	CommentCreateUpdateSerializer,
	CommentDetailSerializer,
	PostCreateUpdateSerializer,
	PostDetailSerializer,
	PostListSerializer, 
	)
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'posts' : reverse('posts-api:post-list', request=request, format=format),
		'comments' : reverse('posts-api:comment-list', request=request, format=format),
		'users' : reverse('users-api:user-list', request=request, format=format)
		})



# comment APIViews
class CommentCreateAPIView(generics.CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateUpdateSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class CommentDeleteAPIView(generics.RetrieveDestroyAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateUpdateSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class CommentDetailAPIView(generics.RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializer
	# permission_classes = (permissions.AllowAny,)


class CommentListAPIView(generics.ListAPIView):
	# queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (permissions.AllowAny,)

	def get_queryset(self):
		queryset = Comment.objects.filter(parent=None)
		try:
			post_id = self.kwargs['post_id']
			if post_id is not None:
				queryset = Comment.objects.filter(
					Q(parent=None),
					Q(post=post_id)
					)
				return queryset
		except:
			pass
		return queryset


class CommentRepliesListAPIView(generics.ListAPIView):
	serializer_class = CommentSerializer

	def get_queryset(self):
		queryset = Comment.objects.filter(parent!=None)
		return queryset


class CommentUpdateAPIView(generics.RetrieveUpdateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateUpdateSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)

# Post APIViews
class PostCreateAPIView(generics.CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
		serializer.save(publish=datetime.datetime.now())


class PostDeleteAPIView(generics.RetrieveDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


class PostDetailAPIView(generics.RetrieveAPIView):
	queryset = Post.objects.published()
	serializer_class = PostDetailSerializer
	permission_classes = (permissions.AllowAny,)
	# lookup_field = 'id'
	

class PostListAPIView(generics.ListAPIView):
	serializer_class = PostListSerializer
	permission_classes = (permissions.AllowAny,)
	
	def get_queryset(self):
		queryset = Post.objects.published()
		query = self.request.query_params.get('q', None)
		if query is not None:
			queryset = Post.objects.search(query)
		return queryset


class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)
		serializer.save(publish=datetime.datetime.now())