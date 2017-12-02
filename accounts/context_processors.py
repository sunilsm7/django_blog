from django.contrib.auth.models import User


def user_messages_list(request):
	c = {}
	if request.user.is_authenticated():
		c["message_user_list"] = User.objects.all()
	return c