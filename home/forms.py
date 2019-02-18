from django import forms
from home.models import Post, Comment

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
        'class': 'form-control',
        'rows' : 5,
        'placeholder': 'Write something....'
        }
    ))

    title = forms.CharField(widget=forms.TextInput(
        attrs={
        'class': 'form-control',
        'placeholder': 'Title of your post'
        }
    ))

    class Meta:
        model = Post
        fields = ('title','text')

class CommentForm(forms.ModelForm):
        text = forms.CharField(widget=forms.Textarea(
            attrs={
            'class': 'form-control',
            'rows' : '5',
            'placeholder': 'Comment Here'
            }
        ))

        class Meta:
            model=Comment
            fields = ('text',)
