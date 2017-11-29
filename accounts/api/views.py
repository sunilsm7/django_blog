import datetime
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment
from .serializers import (
	SignUpSerializer,
	UserDetailSerializer,
	UserSerializer,
	)

from .permissions import IsSuperUser

# user APIViews
class SignUpIView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer

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


class UserList(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'accounts/user_list.html'
	permission_classes = (permissions.IsAuthenticated, IsSuperUser)
	# serializer_class = UserSerializer

	def get(self, request):
		queryset = User.objects.all()
		serializer = UserSerializer(queryset)
		return Response({'users': queryset, 'serializer':serializer})


class UserDetail(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'accounts/user_detail.html'
	permission_classes = (permissions.IsAuthenticated, IsSuperUser)

	def get(self, request, pk):
		user_detail = get_object_or_404(User, pk=pk)
		serializer = UserDetailSerializer(user_detail, many=True)
		return Response({'user_detail': user_detail, 'serializer': serializer})

	def post(self, request, pk):
		pass
	

@api_view(['POST'])
def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			# login(request, user)
			token, _ = Token.objects.get_or_create(user=user)
			return Response({"token":token.key}, status=HTTP_200_OK)
		else:
			return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		if not username or not password:
			return Response({"error":"missing username or password"})
		user = authenticate(request, username=username, password=password)
		if user is not None:
			# login(request, user)
			token, _ = Token.objects.get_or_create(user=user)
			return Response({"token":token.key}, status=HTTP_200_OK)
		else:
			return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)


# viewset
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	This viewset automatically provides list and detail actions.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer


