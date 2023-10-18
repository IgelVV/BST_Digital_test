from django.core import serializers

from robots.models import Robot


class RobotDeserializer:
    data_template = '[{{"model": "robots.robot", "fields": {fields}}}]'

    def __init__(self, body: bytes) -> None:
        """
        Deserialize json to new Robot obj.

        Handles only one json object, that contains fields with values.
        :raises serializers.base.DeserializationError:
            When body has wrong structure
        :param body: HttpRequest.body.
            Example: b'{"model":"R2","version":"D2",
            "created":"2022-12-31 23:59:59"}'
        """
        encoded_body = str(body, encoding="utf-8")
        self.data = self.data_template.format(fields=encoded_body)

        for obj in serializers.deserialize("json", self.data):
            self.robot: Robot = obj.object
            self.robot.serial = self.robot.model + "-" + self.robot.version
            break

    def validate(self):
        """
        Full clean deserialized object.

        :raises ValidationError: When fields does not pass Robot validation.
        """
        self.robot.full_clean()

    def save(self):
        """
        Save deserialized object to database.
        """
        self.robot.save()
