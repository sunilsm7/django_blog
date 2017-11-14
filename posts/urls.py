from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
	# url(r'^list/$', views.posts_list, name='list'),
	url(r'^list/$', views.PostListView.as_view(), name='list'),
	# url(r'^list/new-post/$', views.new_post, name='new-post'),
	url(r'^list/new-post/$', views.PostCreateView.as_view(), name='new-post'),
	# url(r'^list/(?P<pk>\d+)/edit/$', views.edit_post, name='edit'),
	url(r'^list/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit'),
	# url(r'^list/(?P<pk>\d+)/details/$', views.post_details, name='details'),
	url(r'^list/(?P<pk>\d+)/details/$', views.PostDetailView.as_view(), name='details'),
	# url(r'^list/(?P<pk>\d+)/delete/$', views.delete_post, name='delete'),
	url(r'^list/(?P<pk>\d+)/delete/$', views.PostDeleteView.as_view(), name='delete'),
	url(r'^list/(?P<pk>\d+)/details/(?P<comment_pk>\d+)/replies/$', views.RepliesListView.as_view(), name='replies'),
	url(r'^get_posts/$', views.get_posts, name='get_posts'),

]
