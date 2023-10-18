from django.urls import path
from robots import views

app_name = "robots"

urlpatterns = [
    path("add_robot/", views.AddRobotView.as_view(), name="add_robot"),
]
