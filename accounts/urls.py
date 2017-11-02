from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
	url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	# url(r'^signup/$', views.signup, name='signup'),
	url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
	url(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
]
