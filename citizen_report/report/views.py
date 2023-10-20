from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django_filters.views import FilterView

from .filter import ReportFilter, MyReportFilter
from .forms import ReportForm, UpdateReportForm
from .models import Report
from .utils import assign_clerk
from news.models import NewsPost

User = get_user_model()


def home(request):
    reports = Report.objects.order_by('-created_at')
    news_list = NewsPost.objects.order_by('-created_at')

    return render(request, 'home.html', {'reports': reports, 'news_list':news_list})


class ReportListView(FilterView):
    model = Report
    template_name = 'reports.html'
    context_object_name = 'reports'
    paginate_by = 4
    filterset_class = ReportFilter

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        queryset = super().get_queryset(**kwargs)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(text__icontains=search) |
                Q(category__icontains=search)
            )
        return queryset


class MyReportListView(LoginRequiredMixin, FilterView):
    login_url = 'login'
    model = Report
    template_name = 'my_reports.html'
    context_object_name = 'reports'
    paginate_by = 2
    filterset_class = MyReportFilter

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(**kwargs)
        if user.is_staff:
            queryset = queryset.filter(
                clerk=user
            )
        else:
            queryset = queryset.filter(
                user=user
            )
        return queryset


class ReportCreate(LoginRequiredMixin, generic.CreateView):
    login_url = 'login'
    form_class = ReportForm
    success_url = reverse_lazy("reports")
    template_name = "create.html"

    def get_form_kwargs(self):
        kwargs = super(ReportCreate, self).get_form_kwargs()
        if hasattr(self.request, 'clerk'):
            kwargs['clerk'] = self.request.clerk
        return kwargs

    def form_valid(self, form):
        if self.kwargs.get('clerk'):
            form.instance.clerk = self.kwargs.get('clerk')
        else:
            available_clerks = User.objects.filter(department=form.instance.category).filter(is_staff=True).all()
            form.instance.clerk = available_clerks.annotate(num_reports=Count("assigned_reports")).order_by("num_reports").first()
        form.instance.user = self.request.user
        return super(ReportCreate, self).form_valid(form)

# @login_required
# def create(request):
#     if request.method == 'GET':
#         return render(request, 'create.html', {'form': ReportForm()})
#     elif request.method == 'POST':
#         form = ReportForm(request.POST)
#         if form.is_valid():
#             report = form.save(commit=False)
#             report.user = request.user
#             assign_clerk(report)
#             report.save()
#             return redirect('reports')
#         else:
#             error = 'wrong data in form'
#             return render(request, 'create.html', {'form': ReportForm(request.POST), 'error': error})
#     else:
#         return render(request, "405.html", status=405)


def detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    posts = report.report_posts.all()
    return render(request, 'detail.html', {'report': report,'posts': posts})


@login_required
def update_status(request, report_id):
    if request.user.is_staff:
        report = get_object_or_404(Report, id=report_id, clerk=request.user)
        if request.method == 'GET':
            form = UpdateReportForm(instance=report)
            return render(request, 'update_report.html', {'form': form, 'report': report})
        elif request.method == 'POST':
            form = UpdateReportForm(request.POST, instance=report)
            if form.is_valid():
                report.save()
                return redirect('my_reports')
            else:
                error = 'wrong data in form'
                return render(request, 'update_report.html', {'form': form, 'report': report, 'error': error})
        else:
            return render(request, "405.html", status=405)
    else:
        return render(request, "403.html", status=403)

