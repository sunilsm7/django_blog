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

from posts import views as post_views

urlpatterns = [
	url(r'^$', post_views.HomeView.as_view(), name='home'),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^profiles/', include('accounts.urls', namespace='profiles')),
	url(r'^posts/', include('posts.urls', namespace='posts')),
	url(r'^pages/', include('django.contrib.flatpages.urls', namespace='pages')),
	url(r'^contact/$',post_views.ContactView.as_view() , name='contact'),
	url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)