from django.shortcuts import render
from timesheets_app.models import Company, Employees


class Main:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            companies = Employees.objects.filter(user_id=request.user.id)
            return render(request, 'timesheets/index.html', context={'companies': companies})
        else:
            return render(request, 'timesheets/unauthenticated_index.html')
