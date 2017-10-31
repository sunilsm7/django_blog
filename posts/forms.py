from django import forms
from .models import Post


class NewPostForm(forms.Form):
	title = forms.CharField(max_length=120)
	content = forms.CharField(widget=forms.Textarea)
	draft	= forms.BooleanField(required=False)


class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ['title', 'content', 'draft']

	