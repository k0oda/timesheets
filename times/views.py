from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from times.models import Entry
from projects.models import Project
from manage_app.models import Task
from datetime import date, time, timedelta, datetime

@login_required
def start_timer(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    entry.start_time = datetime.now().time()
    entry.is_active = True
    entry.save()
    return redirect('time', entry.date.year, entry.date.month, entry.date.day)

@login_required
def stop_timer(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    entry.is_active = False

    now = datetime.now()
    now_delta = timedelta(hours=now.hour, minutes=now.minute)
    start_time_delta = timedelta(hours=entry.start_time.hour, minutes=entry.start_time.minute)
    timer_delta = timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)

    entry.timer = (datetime.min + ((now_delta - start_time_delta) + timer_delta)).time()
    entry.start_time = time(0, 0)
    hourly_rate = 0
    for task in entry.project.tasks.all():
        hourly_rate += task.default_hourly_rate
    entry.project.total_earned += entry.timer.hour * hourly_rate
    entry.project.save()
    entry.save()
    return redirect('time', entry.date.year, entry.date.month, entry.date.day)

@login_required
def add_entry(request, year, month, day):
    if request.method.lower() == 'post':
        _date = date(year, month, day)
        project = get_object_or_404(Project, name=request.POST.get('project'), company=request.user.company)
        task = get_object_or_404(Task, name=request.POST.get('task'), company=request.user.company)
        notes = request.POST.get('notes')
        timer = request.POST.get('timer')
        new_entry = Entry.objects.create(
            company=request.user.company,
            user=request.user,
            date=_date,
            project=project,
            task=task,
            notes=notes,
            timer=timer
        )
        new_entry.save()
    return redirect('time', year, month, day)

@login_required
def edit_entry(request, pk):
    if request.method.lower() == 'post':
        entry = get_object_or_404(Entry, company=request.user.company, pk=pk)
        entry.project = get_object_or_404(Project, name=request.POST.get('project'), company=request.user.company)
        entry.task = get_object_or_404(Task, name=request.POST.get('task'), company=request.user.company)
        entry.notes = request.POST.get('notes')
        entry.timer = request.POST.get('timer')
        entry.save()
    return redirect('time', entry.date.year, entry.date.month, entry.date.day)

@login_required
def delete_entry(request, pk):
    entry = get_object_or_404(Entry, company=request.user.company, pk=pk)
    
    hourly_rate = 0
    for task in entry.project.tasks.all():
        hourly_rate += task.default_hourly_rate
    entry.project.total_earned -= entry.timer.hour * hourly_rate
    entry.project.save()
    entry.delete()
    return redirect('time', entry.date.year, entry.date.month, entry.date.day)

@login_required
def time(request, year=0, month=0, day=0):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    if year == 0 and month == 0 and day == 0:
        _date = date.today()
    else:
        _date = date(year, month, day)

    start_of_week = _date - timedelta(days=_date.weekday())
    week = []
    totals = []
    week_total = datetime(year=date.min.year, month=date.min.month, day=date.min.day, hour=0, minute=0)
    for i in range(0, 7):
        total = datetime(year=date.min.year, month=date.min.month, day=date.min.day, hour=0, minute=0)
        day_entries = Entry.objects.filter(date=start_of_week + timedelta(days=i), company=request.user.company)
        for entry in day_entries:
            total += timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)
            week_total += timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)
        totals.append(total)
        week.append(start_of_week + timedelta(days=i))

    week_total = week_total.time
    next_date = _date + timedelta(days=1)
    previous_date = _date - timedelta(days=1)

    pages = Paginator(Entry.objects.filter(date=_date, company=request.user.company, user=request.user), settings.ITEMS_PER_PAGE)
    entries = pages.page(page).object_list

    projects = Project.objects.filter(company=request.user.company)
    tasks = Task.objects.filter(company=request.user.company)
    today = date.today()
    return render(request, 'times/time.html', context={
        'date': _date,
        'pages': pages,
        'current_page': page,
        'entries': entries,
        'projects': projects,
        'tasks': tasks,
        'week': week,
        'today': today,
        'next_date': next_date,
        'previous_date': previous_date,
        'totals': totals,
        'week_total': week_total,
        'date_total': totals[_date.weekday()]
    })

@login_required
def pick_date(request):
    _date = request.POST.get('date').split('-')
    _date = date(int(_date[0]), int(_date[1]), int(_date[2]))
    return redirect('time', _date.year, _date.month, _date.day)
