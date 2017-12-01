from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
	url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
	url(r'^post_list/$', views.PostListView.as_view(), name='post-list'),
	url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
	url(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html', success_url=reverse_lazy('accounts:password_change_done')),
		name='password_change'),
	url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
		name='password_change_done'),
	url(r'^reset/$', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
	url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<activation_key>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		views.activate, name='activate'),

	url(r'^validate_username/$', views.validate_username, name='validate_username'),
	url(r'^add_remove_author/$', views.add_remove_author, name='add_remove_author'),
	url(r'^write_for_us/$', views.write_for_us, name='write_for_us'),
	url(r'^post_approved_change/$', views.post_approved_change, name='post_approved_change'),
]