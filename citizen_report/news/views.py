from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import NewsPostCreationForm
from .models import NewsPost
from report.models import Report


# class NewsPostList(generic.ListView):
#     model = NewsPost
#     queryset = NewsPost.objects.filter(report=report).all().order_by('-created_at')
#     template_name = 'news.html'


class NewsPostCreate(generic.CreateView):
    form_class = NewsPostCreationForm
    success_url = reverse_lazy("home")
    template_name = "create_post.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['report'].limit_choices_to = {'clerk': self.request.user}
        return modelform

    def form_valid(self, form):
        user = self.request.user
        form.instance.clerk = user if user else None
        return super(NewsPostCreate, self).form_valid(form)


def news(request, report_id):

    report = Report.objects.filter(id=report_id).first()

    posts = report.report_posts.all()

    return render(request, 'news.html',{'newspost_list':posts, 'report':report})
