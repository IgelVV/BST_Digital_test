import xlsxwriter
from typing import Union
from datetime import datetime, timedelta

from django.db.models import Count, QuerySet
from django.utils.translation import gettext as _
from django.http import HttpResponse

from robots.models import Robot


class RobotService:
    def get_weekly_report_as_response(
            self, file_name: str = None) -> HttpResponse:
        """
        Create a report in xlsx format about robots created last week.

        HttpResponse is used as file-like object, to store report.
        :param file_name: name for report.
        :return: response
        """
        if file_name is None:
            file_name = "weekly_robot_report.xlsx"
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument"
                         ".spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f"attachment; filename={file_name}"
        robot_data = self._get_count_produced_for(for_days=7)
        print(robot_data)
        response = self.create_xlsx_report(robot_data, response)
        return response

    def create_xlsx_report(
            self, robots: QuerySet,
            file: Union[HttpResponse, str],
    ) -> Union[HttpResponse, str]:
        """
        Write xlsx report to response or file.

        :param robots: QuerySet values with data about Robots, required keys:
            "model", "version", "version_count"
        :param file: HttpRequest or path to file to write in the report.
        :return: request or file_path
        """
        with xlsxwriter.Workbook(file) as workbook:
            previous_model = None
            row = 0
            for robot in robots:
                if robot["model"] != previous_model:
                    worksheet_model = workbook.add_worksheet(robot["model"])
                    previous_model = robot["model"]
                    row = 0
                    row_data = [_("Модель"), _("Версия"),
                                _("Количество за неделю")]
                    worksheet_model.write_row(row, 0, row_data, )
                    row += 1
                else:
                    worksheet_model = workbook.sheetnames[robot["model"]]

                row_data = [robot["model"], robot["version"],
                            robot["version_count"]]
                worksheet_model.write_row(row, 0, row_data)
                row += 1
        return file

    def _get_count_produced_for(self, for_days: int) -> QuerySet:
        """
        Get query set of Robots grouped by version.

        :param for_days: period of time to this moment
        :return: <QuerySet [
            {'model': '13', 'version': '11', 'version_count': 1}, ...].
            'version_count' - amount of robots with specific
            'model' and 'version'.
        """
        return Robot.objects \
            .filter(created__gte=datetime.now() - timedelta(days=for_days)) \
            .values("model", "version") \
            .annotate(version_count=Count("version")) \
            .order_by("model")
