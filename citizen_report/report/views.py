from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Report
from .forms import ReportForm


def home(request):
    return render(request, 'home.html')


def show_reports(request):
    user_reports = Report.objects.filter(user=request.user)
    return render(request, 'reports.html', {'user_reports': user_reports})


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
        error = 'method not allowed'
        # TODO: HttpResponse('405 - do zmiany!!!') or Response(status=status.HTTP_405) EXPLORE DOCS
        return render(request, 'create.html', {'error': error})


def detail(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    return render(request, 'detail.html', {'report': report})
            # TODO: user.is_staff - this view or new one? for editing status of report - guidance needed, @login_required to add
