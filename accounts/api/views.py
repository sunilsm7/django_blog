import datetime
from rest_framework import generics, permissions, parsers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment
from .serializers import (
	AuthTokenSerializer,
	LoginSerializer,
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
	

class UserLoginAPIView(APIView):
	permission_classes = [permissions.AllowAny]
	serializer_class = LoginSerializer
	
	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = LoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			headers = {
				'Authorization': 'Token ' + new_data['token'],
			}
			return Response(new_data, headers=headers, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
	queryset = User.objects.all()

	def get(self, request, format=None):
		try:
			request.user.auth_token.delete()
		except:
			pass
		return Response(status=HTTP_200_OK)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user':user.username})
