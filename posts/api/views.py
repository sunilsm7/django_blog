import datetime
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.db.models import Q
from django.http import JsonResponse

from posts.models import Post, Comment
from .serializers import (
    CommentSerializer,
    CommentCreateUpdateSerializer,
    CommentDetailSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostStatusUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly
from accounts.api.permissions import IsSuperUser

from posts.search import search, search_all


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'posts': reverse('posts-api:post-list', request=request, format=format),
        'comments': reverse('posts-api:comment-list', request=request, format=format),
        'users': reverse('users-api:user-list', request=request, format=format),
        # 'login' : reverse('rest_framework:login', request=request, format=format),
    })


# comment APIViews
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = CommentCreateUpdateSerializer
    serializer_class = CommentSerializer
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
        except Exception:
            pass
        return queryset


class CommentRepliesListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(parent != None)  # noqa
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
    queryset = Post.objects.all()
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


class PostStatusUpdate(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostStatusUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)

    def perform_update(self, serializer):
        # serializer.save(user=self.request.user)
        serializer.save(publish=datetime.datetime.now())


def search_posts(request):
    query = request.GET.get('q')
    if query is not None:
        results = search(query)
        return JsonResponse(results.to_dict())
    return JsonResponse({'message': 'no query to search', 'status': 200})


def post_list(request):
    results = search_all()
    return JsonResponse(results.to_dict())
