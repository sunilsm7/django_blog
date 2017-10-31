from django import template
from posts.models import Post

register = template.Library()

def last_ten_updated_posts():
	latest_ten_post = Post.objects.filter(draft=False).order_by('-updated')[:10]
	return {'latest_ten_post':latest_ten_post}
