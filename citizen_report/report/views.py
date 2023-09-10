from django.shortcuts import render, redirect, get_object_or_404

from .models import Report
from .forms import ReportForm
# Create your views here.

def home(request):
    return render(request, 'home.html')


def show_reports(request):
    userReports = Report.objects.filter(user=request.user)
    current = Report.objects.filter(user=request.user, created_at__isnull=True)
    return render(request, 'reports.html', {'current': current, 'userReports': userReports})


def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form': ReportForm()})
    else: #POST
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('tasks')
        else:
            error = 'something is wrong'
            return render(request, 'create.html', {'form': ReportForm(), 'error': error})


def detail(request, reportId):
    report = get_object_or_404(Report, id=reportId, user=request.user)
    # user = get_object_or_404(User, id=userId)
    if request.method == 'GET':
        form = ReportForm(instance=report)
        return render(request, 'detail.html', {'form': form, 'report':report})
    else: #POST
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            # if User.is_staff:
            form.save()
            return redirect('tasks')
        else:
            error = 'something went wrong'
            return render(request, 'detail.html', {'form': form, 'report':report, 'error': error})

