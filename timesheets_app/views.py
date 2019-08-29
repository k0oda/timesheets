from django.shortcuts import render


class Main:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            return render(request, 'timesheets/index.html')
        else:
            return render(request, 'timesheets/unauthenticated_index.html')
