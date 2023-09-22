from django import forms

from .models import NewsPost, Comment


class NewsPostCreationForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ('report', 'title', 'text', 'image')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'text')


