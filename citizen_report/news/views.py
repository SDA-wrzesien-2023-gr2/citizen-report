from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import NewsForm, NewsCommentForm
from .models import NewsPost


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

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['report'].limit_choices_to = {'clerk': self.request.user}
        return modelform

    def form_valid(self, form):
        user = self.request.user
        form.instance.clerk = user if user else None
        return super(NewsPostCreate, self).form_valid(form)


class NewsCommentCreate(LoginRequiredMixin, generic.CreateView):
    form_class = NewsCommentForm
    template_name = "add_comment_to_news.html"

    def form_valid(self, form):
        user = self.request.user
        post = get_object_or_404(NewsPost, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.user = user if user else None
        return super(NewsCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_news', kwargs={'pk': self.kwargs.get('pk')})

