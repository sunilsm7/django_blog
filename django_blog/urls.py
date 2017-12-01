"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from posts.api import  views as api_views
from posts import views as post_views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'posts', api_views.PostViewSet)
# router.register(r'users', api_views.UserViewSet)
# router.register(r'comment', api_views.CommentViewSet)

urlpatterns = [
	url(r'^$', post_views.HomeView.as_view(), name='home'),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^profiles/', include('accounts.urls', namespace='profiles')),
	url(r'^posts/', include('posts.urls', namespace='posts')),
	url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
	url(r'^api/$', api_views.api_root),
	url(r'^api/posts/', include('posts.api.urls', namespace='posts-api')),
	url(r'^api/users/', include('accounts.api.urls', namespace='users-api')),
	#url(r'^posts-api/', include(router.urls)),
	url(r'^pages/', include('django.contrib.flatpages.urls', namespace='pages')),
	url(r'^contact/$',post_views.ContactView.as_view() , name='contact'),
	url(r'^admin/', admin.site.urls),
]

urlpatterns += [
	url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)