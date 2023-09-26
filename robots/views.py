from django.views import View
from django.http import HttpRequest, HttpResponse


class WeeklyReportView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(status=200)
