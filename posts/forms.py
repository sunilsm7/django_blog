from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content', 'read_time', 'draft',]
		widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder':'What is in your mind?'}),
            'read_time': forms.NumberInput(attrs={'min':0}),
        }


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content',]
		widgets = {
			'content': forms.Textarea(attrs={'rows': 2, 'placeholder':'What is in your mind?', 'class':'textarea-content'}),	
		}


class ContactForm(forms.Form):
	name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter name',}))
	subject = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Enter subject for future reference .',}))
	email = forms.CharField(max_length=120, widget=forms.EmailInput(attrs={'placeholder':'Enter valid email id. eg. abc@gmail.com',}))
	message = forms.CharField(widget = forms.Textarea(attrs={'placeholder':'what is in your mind ?',}))



class SearchForm(forms.Form):
	content = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder':'Search Posts',}))