from django.conf.urls import url
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^$', views.PostListAPIView.as_view(), name='post-list'),
	url(r'^create/$', views.PostCreateAPIView.as_view(), name='post-create'),
	#url(r'^posts/(?P<slug>[\w-]+)/detail/$', views.PostDetailAPIView.as_view(), name='post-detail'),
	url(r'^(?P<pk>[0-9]+)/detail$', views.PostDetailAPIView.as_view(), name='post-detail'),	
	url(r'^(?P<pk>[0-9]+)/update/$', views.PostUpdateAPIView.as_view(), name='post-update'),
	url(r'^(?P<pk>[0-9]+)/status_update/$', views.PostStatusUpdate.as_view(), name='post-status-update'),
	url(r'^(?P<pk>[0-9]+)/delete/$', views.PostDeleteAPIView.as_view(), name='post-delete'),
	url(r'^comments/$', views.CommentListAPIView.as_view(), name='comment-list'),
	url(r'^comments/(?P<post_id>[0-9]+)/post_comments/$', views.CommentListAPIView.as_view(), name='post-comment-list'),
	url(r'^comments/create/$', views.CommentCreateAPIView.as_view(), name='comment-create'),
	url(r'^comments/(?P<pk>[0-9]+)/detail/$', views.CommentDetailAPIView.as_view(), name='comment-detail'),
	url(r'^comments/(?P<pk>[0-9]+)/update/$', views.CommentUpdateAPIView.as_view(), name='comment-update'),
	url(r'^comments/(?P<pk>[0-9]+)/delete/$', views.CommentDeleteAPIView.as_view(), name='comment-delete'),
	# url(r'^comments/(?P<pk>[0-9]+)/reply/$', views.CommentRepliesListAPIView.as_view(), name='comment-reply'),
	url(r'^search/$', views.search_posts, name='search'),
    url(r'^list/$', views.post_list, name='list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)