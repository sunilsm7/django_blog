import datetime
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from posts.models import Post, Comment
from .serializers import (
	UserCreateSerializer,
	UserDetailSerializer,
	UserSerializer,
	)


# user APIViews
class UserCreateAPIView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer

	def perform_create(self, serializer):
		serializer.save()

# class UserDeleteAPIView(generics.RetrieveDestroyAPIView):
# 	queryset = User.objects.all()
# 	serializer_class = UserDetailSerializer
# 	# permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class UserDetailAPIView(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer


class UserListAPIView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

# viewset
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	This viewset automatically provides list and detail actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
