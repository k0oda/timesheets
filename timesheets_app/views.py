from django.shortcuts import render


class Main:
    @staticmethod
    def main(request):
        return render(request, 'timesheets/index.html')
