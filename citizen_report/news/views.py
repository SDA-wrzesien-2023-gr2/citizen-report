from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import NewsPostCreationForm, CommentForm
from .models import NewsPost


class NewsPostList(generic.ListView):
    model = NewsPost
    template_name = 'news.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        return queryset.filter(report_id=self.kwargs['pk'])


class PostDetail(generic.DetailView):
    model = NewsPost
    template_name = 'detail_post.html'


class NewsPostCreate(LoginRequiredMixin, generic.CreateView):
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


def add_comment_to_post(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    comments = post.comments.filter(approved_comment=True)
    comment = None
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'post': post,
                                                        'comments': comments,
                                                        'comment': comment,
                                                        'form': form})
