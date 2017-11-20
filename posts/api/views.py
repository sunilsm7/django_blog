from django.http import Http404, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from django.contrib.auth.models import User
from posts.models import Post
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users' : reverse('posts-api:user-list', request=request, format=format),
		'posts' : reverse('posts-api:post-list', request=request, format=format),
		'comments' : reverse('posts-api:comment-list', request=request, format=format)
		})


# viewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	This viewset automatically provides list and detail actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides list, create, retrieve,
	update and destroy actions.
	"""
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

# user APIViews
class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


# Generic APIViews
class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



# # using mixins
# class SnippetListMixinView(mixins.ListModelMixin,
# 						mixins.CreateModelMixin,
# 						generics.GenericAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostSerializer

# 	def get(self, request, *args, **kwargs):
# 		return self.list(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
# 		return self.create(request, *args, **kwargs)


# class PostDetailMixinView(mixins.RetrieveModelMixin, 
# 						mixins.UpdateModelMixin, 
# 						mixins.DestroyModelMixin, 
# 						generics.GenericAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostSerializer

# 	def get(self, request, *args, **kwargs):
# 		return self.retrieve(request, *args, **kwargs)

# 	def put(self, request, *args, **kwargs):
# 		return self.update(request, *args, **kwargs)

# 	def delete(self, request, *args, **kwargs):
# 		return self.destroy(request, *args, **kwargs)


# # class based API views
# class PostList(APIView):
# 	"""
# 	List all posts, or create a new post.
# 	"""
# 	def get(self, request, format=None):
# 		posts = Post.objects.all()
# 		serializer = PostSerializer(posts, many=True)
# 		return Response(serializer.data)

# 	def post(self, request, format=None):
# 		serializer = PostSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
# 	"""
# 	Retrieve, update or delete a post instance.
# 	"""
# 	def get_object(self, pk):
# 		try:
# 			return Post.objects.get(pk=pk)
# 		except Post.DoesNotExist:
# 			raise Http404

# 	def get(self, request, pk, format=None):
# 		post = self.get_object(pk)
# 		serializer = PostSerializer(post)
# 		return Response(serializer.data)

# 	def put(self, request, pk, format=None):
# 		post = self.get_object(pk)
# 		serializer = PostSerializer(post, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 	def delete(self, request, pk , format=None):
# 		post = self.get_object(pk)
# 		post.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET','POST'])
# def post_list(request, format=None):
# 	"""
# 	List all posts or create a new post.
# 	"""
# 	if request.method == 'GET':
# 		posts = Post.objects.all()
# 		serializer = PostSerializer(posts, many=True)
# 		return Response(serializer.data)

# 	elif request.method == 'POST':
# 		serializer = PostSerializer(data=request.data)

# 		if serializer.is_valid():
# 			serializer.save()
# 			return	Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','PUT','DELETE'])
# def post_detail(request, pk, format=None):
# 	"""
# 	list, update or delete post
# 	"""
# 	try:
# 		post = Post.objects.get(pk=pk)
# 	except Post.DoesNotExist:
# 		return Response(status=HTTP_404_NOT_FOUND)

# 	if request.method == 'GET':
# 		serializer = PostSerializer(post)
# 		return Response(serializer.data)

# 	elif request.method == 'PUT':
# 		serializer = PostSerializer(post, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# 	elif request.method == 'DELETE':
# 		post.delete()
# 		return HttpResponse(status=HTTP_204_NO_CONTENT)

