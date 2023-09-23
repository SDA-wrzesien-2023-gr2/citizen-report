from django import forms

from .models import NewsPost, NewsComment


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ('report', 'title', 'text', 'image')


class NewsCommentForm(forms.ModelForm):

    class Meta:
        model = NewsComment
        fields = ('text',)


