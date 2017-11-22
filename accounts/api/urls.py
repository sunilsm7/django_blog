from django.conf.urls import url
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^$', views.UserListAPIView.as_view(), name = 'user-list'),
	url(r'^create/$', views.UserCreateAPIView.as_view(), name = 'user-create'),
	url(r'^(?P<pk>[0-9])+/detail/$', views.UserDetailAPIView.as_view(), name = 'user-detail'),
	# url(r'^(?P<pk>[0-9])+/delete/$', views.UserDeleteAPIView.as_view(), name = 'user-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)