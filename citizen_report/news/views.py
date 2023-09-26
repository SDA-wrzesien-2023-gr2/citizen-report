from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import NewsForm, NewsCommentForm
from .models import NewsPost
from report.models import Report


class NewsPostList(generic.ListView):
    model = NewsPost
    template_name = 'news.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(report_id=self.kwargs['pk'])


class NewsPostDetail(generic.DetailView):
    model = NewsPost
    template_name = 'detail_news.html'


class NewsPostCreate(LoginRequiredMixin, generic.CreateView):
    form_class = NewsForm
    success_url = reverse_lazy("my_reports")
    template_name = "create_news.html"

    def form_valid(self, form):
        form.instance.report = get_object_or_404(Report, pk=self.kwargs['pk'])
        form.instance.clerk = self.request.user
        return super(NewsPostCreate, self).form_valid(form)


class NewsCommentCreate(LoginRequiredMixin, generic.CreateView):
    form_class = NewsCommentForm
    template_name = "add_comment_to_news.html"

    def form_valid(self, form):
        form.instance.post = get_object_or_404(NewsPost, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super(NewsCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_news', kwargs={'pk': self.kwargs.get('pk')})

