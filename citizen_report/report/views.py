from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReportForm, UpdateReportForm
from .models import Report


def home(request):
    return render(request, 'home.html')


def list_reports(request):
    reports = Report.objects.all()
    return render(request, 'reports.html', {'reports': reports})


@login_required
def my_reports(request):
    reports = Report.objects.filter(clerk=request.user).all()
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
            report.save()
            return redirect('reports')
        else:
            error = 'wrong data in form'
            return render(request, 'create.html', {'form': ReportForm(request.POST), 'error': error})
    else:
        return render(request, "405.html", status=405)


@login_required
def detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    posts = report.report_posts.all()
    return render(request, 'detail.html', {'report': report,'posts':posts})


@login_required
def update_status(request, report_id):
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
