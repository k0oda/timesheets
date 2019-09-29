from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from timesheets_app.models import Company, Entry, Project, Task
from authentication.models import UserProfile
from timesheets_app.forms import CreateCompanyForm, DatePicker
from datetime import date, time, timedelta, datetime


class Main:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            company_id = UserProfile.objects.get(username=request.user.username).company_id
            if Company.objects.filter(pk=company_id).exists():
                company = Company.objects.get(pk=company_id)
            else:
                company = 0
            return render(request, 'timesheets/company_header.html', context={'company': company})
        else:
            return render(request, 'timesheets/unauthenticated.html')

    @staticmethod
    @login_required
    def new_company(request):
        if request.method.lower() == 'post':
            form = CreateCompanyForm(request.POST)
            company = form.save(commit=False)
            user = UserProfile.objects.get(username=request.user.username)
            company.save()
            user.company_id = company.pk
            user.save()
            return redirect('/')
        else:
            form = CreateCompanyForm()
        return render(request, 'timesheets/new_company.html', {'form': form})


class CompanyPanel:
    @staticmethod
    @login_required
    def start_timer(request, entry_id):
        entry = Entry.objects.get(pk=entry_id)
        entry.start_time = datetime.now().time()
        entry.is_active = True
        entry.save()
        return redirect('time', entry.date.year, entry.date.month, entry.date.day)

    @staticmethod
    @login_required
    def stop_timer(request, entry_id):
        entry = Entry.objects.get(pk=entry_id)
        entry.is_active = False

        now = datetime.now()
        now_delta = timedelta(hours=now.hour, minutes=now.minute)
        start_time_delta = timedelta(hours=entry.start_time.hour, minutes=entry.start_time.minute)
        timer_delta = timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)

        entry.timer = (datetime.min + ((now_delta - start_time_delta) + timer_delta)).time()
        entry.start_time = time(0, 0)
        entry.save()
        return redirect('time', entry.date.year, entry.date.month, entry.date.day)

    @staticmethod
    @login_required
    def add_entry(request, year, month, day):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            _date = date(year, month, day)
            project = Project.objects.get(name=request.POST.get('project'), company=company)
            task = Task.objects.get(name=request.POST.get('task'), company=company)
            notes = request.POST.get('notes')
            timer = request.POST.get('timer')
            new_entry = Entry.objects.create(
                company=company,
                date=_date,
                project=project,
                task=task,
                notes=notes,
                timer=timer
            )
            new_entry.save()
        return redirect('time', year, month, day)

    @staticmethod
    @login_required
    def edit_entry(request, pk):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            entry = Entry.objects.get(company=company, pk=pk)
            entry.project = Project.objects.get(name=request.POST.get('project'), company=company)
            entry.task = Task.objects.get(name=request.POST.get('task'), company=company)
            entry.notes = request.POST.get('notes')
            entry.timer = request.POST.get('timer')
            entry.save()
        return redirect('time', entry.date.year, entry.date.month, entry.date.day)

    @staticmethod
    @login_required
    def delete_entry(request, pk):
        company = Company.objects.get(pk=request.user.company_id)
        entry = Entry.objects.get(company=company, pk=pk)
        entry.delete()
        return redirect('time', entry.date.year, entry.date.month, entry.date.day)

    @staticmethod
    @login_required
    def time(request, year=0, month=0, day=0):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0

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
            day_entries = Entry.objects.filter(date=start_of_week + timedelta(days=i), company=company)
            for entry in day_entries:
                total += timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)
                week_total += timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)
            totals.append(total)
            week.append(start_of_week + timedelta(days=i))

        week_total = week_total.time
        next_date = _date + timedelta(days=1)
        previous_date = _date - timedelta(days=1)

        entries = Entry.objects.filter(date=_date, company=company)
        projects = Project.objects.all()
        tasks = Task.objects.all()
        today = date.today()
        return render(request, 'timesheets/company_panel/time.html', context={
            'company': company,
            'date': _date,
            'entries': entries,
            'projects': projects,
            'tasks': tasks,
            'week': week,
            'today': today,
            'next_date': next_date,
            'previous_date': previous_date,
            'totals': totals,
            'week_total': week_total,
            'date_total': totals[_date.weekday()],
            'datepicker': DatePicker()
        })

    @staticmethod
    @login_required
    def pick_date(request):
        _date = request.POST.get('date').split('-')
        _date = date(int(_date[0]), int(_date[1]), int(_date[2]))
        return redirect('time', _date.year, _date.month, _date.day)

    @staticmethod
    @login_required
    def expenses(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/expenses.html', context={'company': company})

    @staticmethod
    @login_required
    def projects(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/projects.html', context={'company': company})

    @staticmethod
    @login_required
    def team(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/team.html', context={'company': company})

    @staticmethod
    @login_required
    def invoices(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/invoices.html', context={'company': company})

    @staticmethod
    @login_required
    def manage(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/manage.html', context={'company': company})
