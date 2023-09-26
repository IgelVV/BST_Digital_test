from django.views import View
from django.http import HttpRequest, HttpResponse

from robots.services import RobotService


class WeeklyReportView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Download report for last 7 days about Robot production."""
        response = RobotService().get_weekly_report_as_response()
        return response
