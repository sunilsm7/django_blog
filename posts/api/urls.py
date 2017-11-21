from django.conf.urls import url
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
# from posts.api.views import UserViewSet, PostViewSet, api_root


# post_list = PostViewSet.as_view({
# 	'get':'list',
# 	'post':'create'
# 	})

# post_detail = PostViewSet.as_view({
# 	'get':'retrieve',
# 	'put':'update',
# 	'patch':'partial_update',
# 	'delete':'destroy',
# 	})

# user_list = UserViewSet.as_view({
# 	'get':'list'
# 	})

# user_detail = UserViewSet.as_view({
# 	'get':'retrieve'
# 	})

urlpatterns = [
	url(r'^$', views.PostListAPIView.as_view(), name='post-list'),
	url(r'^create/$', views.PostCreateAPIView.as_view(), name='post-create'),
	#url(r'^posts/(?P<slug>[\w-]+)/detail/$', views.PostDetailAPIView.as_view(), name='post-detail'),
	url(r'^(?P<pk>[0-9]+)/$', views.PostDetailAPIView.as_view(), name='post-detail'),	
	url(r'^(?P<pk>[0-9]+)/update/$', views.PostUpdateAPIView.as_view(), name='post-update'),
	url(r'^(?P<pk>[0-9]+)/delete/$', views.PostDeleteAPIView.as_view(), name='post-delete'),
	url(r'^comments/$', views.CommentListAPIView.as_view(), name='comment-list'),
	url(r'^comments/create/$', views.CommentCreateAPIView.as_view(), name='comment-create'),
	url(r'^comments/(?P<pk>[0-9]+)/detail/$', views.CommentDetailAPIView.as_view(), name='comment-detail'),
	url(r'^comments/(?P<pk>[0-9]+)/update/$', views.CommentUpdateAPIView.as_view(), name='comment-update'),
	url(r'^comments/(?P<pk>[0-9]+)/delete/$', views.CommentDeleteAPIView.as_view(), name='comment-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)