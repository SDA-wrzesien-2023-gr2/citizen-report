from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django_filters.views import FilterView

from .filter import ReportFilter
from .forms import ReportForm, UpdateReportForm
from .models import Report
from .utils import assign_clerk

def home(request):
    reports = Report.objects.order_by('-created_at')[:5]
    return render(request, 'home.html', {'reports': reports})


class ReportListView(FilterView):
    model = Report
    template_name = 'reports.html'
    context_object_name = 'reports'
    paginate_by = 6
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


@login_required
def my_reports(request):
    if request.user.is_staff:
        reports = Report.objects.filter(clerk=request.user).all()
    else:
        reports = Report.objects.filter(user=request.user).all()
    return render(request, 'my_reports.html', {'reports': reports})


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form': ReportForm()})
    elif request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            assign_clerk(report)
            report.save()
            return redirect('reports')
        else:
            error = 'wrong data in form'
            return render(request, 'create.html', {'form': ReportForm(request.POST), 'error': error})
    else:
        return render(request, "405.html", status=405)


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
                return redirect('reports')
            else:
                error = 'wrong data in form'
                return render(request, 'update_report.html', {'form': form, 'report': report, 'error': error})
        else:
            return render(request, "405.html", status=405)
    else:
        return render(request, "403.html", status=403)

