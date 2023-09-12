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
        return HttpResponse('405 - do zmiany!!!')
        # return Response(status=status.HTTP_405)
        # return render(request, 'create.html', {'form': ReportForm(request.POST), 'error': error})


def detail(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    form = ReportForm(instance=report)
    if request.method == 'GET':
        return render(request, 'detail.html', {'form': form, 'report': report})
    elif request.method == 'POST':
        if form.is_valid():
            # TODO: user.is_staff
            form.save()
            return redirect('tasks')
        else:
            error = 'something went wrong'
            return render(request, 'detail.html', {'form': form, 'report': report, 'error': error})
    else:
        error = 'something went wrong'
        return render(request, 'detail.html', {'form': form, 'report': report, 'error': error})
