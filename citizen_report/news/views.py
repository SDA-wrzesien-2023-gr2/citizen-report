from django.shortcuts import render

from .models import NewsPost


# Create your views here.

def news(request, report):

    posts = NewsPost.objects.filter(report=report).all()

    return render(request, 'news.html',{'posts':posts})
