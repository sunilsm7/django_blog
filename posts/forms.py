from django import forms
from .models import Post, Comment


class NewPostForm(forms.Form):
	title = forms.CharField(max_length=120)
	content = forms.CharField(widget=forms.Textarea)
	draft	= forms.BooleanField(required=False)


class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ['title', 'content', 'draft']
		widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder':'What is in your mind?'}),
        }


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['content',]
		widgets = {
			'content': forms.Textarea(attrs={'rows': 5, 'placeholder':'What is in your mind?'}),	
		}