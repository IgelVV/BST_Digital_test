from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse


class AddRobotView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        data = request.POST

        return HttpResponse(str(data), status=200)
