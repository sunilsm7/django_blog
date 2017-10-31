from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
	url(r'^list/$', views.posts_list, name='list'),
	url(r'^list/new-post/$', views.new_post, name='new-post'),
	url(r'^list/(?P<pk>\d+)/edit/$', views.edit_post, name='edit'),
	url(r'^list/(?P<pk>\d+)/details/$', views.post_details, name='details'),
	url(r'^list/(?P<pk>\d+)/delete/$', views.delete_post, name='delete'),

]
