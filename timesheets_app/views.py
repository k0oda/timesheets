from django.shortcuts import render
from timesheets_app.models import Company
from authentication.models import UserProfile


class Main:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            company_id = UserProfile.objects.get(username=request.user.username).company_id
            if Company.objects.filter(pk=company_id).exists():
                company = Company.objects.get(pk=company_id)
            else:
                company = 0
            return render(request, 'timesheets/index.html', context={'company': company})
        else:
            return render(request, 'timesheets/unauthenticated_index.html')
