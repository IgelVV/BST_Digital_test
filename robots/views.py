from django.core import serializers
from django.core.exceptions import ValidationError
from django.views import View
from django.http import HttpRequest, HttpResponse


class AddRobotView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        data = f'[{{"model": "robots.robot", ' \
               f'"fields": {str(request.body, encoding="utf-8")}}}]'
        try:
            for obj in serializers.deserialize("json", data):
                robot = obj.object
                robot.serial = robot.model + "-" + robot.version
                try:
                    robot.full_clean()
                    robot.save()
                except ValidationError as e:
                    print(e.__repr__())
                    return HttpResponse(e, status=403)
                break
        except serializers.base.DeserializationError as e:
            print(e.__repr__())
            return HttpResponse(e, status=403)

        return HttpResponse(status=200)
