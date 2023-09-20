from django.shortcuts import render
from django.views import generic

from .models import NewsPost
from report.models import Report



# class NewsPostList(generic.ListView):
#     model = NewsPost
#     queryset = NewsPost.objects.filter(report=report).all().order_by('-created_at')
#     template_name = 'news.html'



def news(request, report_id):

    report = Report.objects.filter(id=report_id).first()

    posts = report.report_posts.all()

    return render(request, 'news.html',{'newspost_list':posts, 'report':report})
