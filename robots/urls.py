from django.urls import path
from robots import views

app_name = "robots"

urlpatterns = [
    path(
        "weekly_report/",
        views.WeeklyReportView.as_view(),
        name="weekly_report"
    ),
]