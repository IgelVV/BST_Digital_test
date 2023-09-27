from django.core.serializers.base import DeserializationError
from django.core.exceptions import ValidationError
from django.views import View
from django.http import HttpRequest, HttpResponse

from robots.deserializer import RobotDeserializer


class AddRobotView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            deserializer = RobotDeserializer(request.body)
            deserializer.validate()
            deserializer.save()
        except DeserializationError as e:
            print(e.__repr__())
            return HttpResponse(e, status=400)
        except ValidationError as e:
            print(e.__repr__())
            return HttpResponse(e, status=400)

        return HttpResponse(status=201)
