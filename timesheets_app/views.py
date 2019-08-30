from django.shortcuts import render
from timesheets_app.models import Company
from authentication.models import UserProfile


class Main:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            company_id = UserProfile.objects.get(username=request.user.username).company_id
            company = Company.objects.get(pk=company_id)
            return render(request, 'timesheets/index.html', context={'company': company})
        else:
            return render(request, 'timesheets/unauthenticated_index.html')
