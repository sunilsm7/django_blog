from django.conf.urls import url
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from posts.api.views import UserViewSet, PostViewSet, api_root


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

# urlpatterns = [
# 	url(r'^$', api_root),
# 	url(r'^posts/$', post_list, name='post-list'),
# 	url(r'^posts/(?P<pk>[0-9]+)/detail/$', post_detail, name='post-detail'),
# 	url(r'^users/$', user_list, name = 'user-list'),
# 	url(r'^users/(?P<pk>[0-9])+/$', user_detail, name = 'user-detail'),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)