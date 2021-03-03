import os
from datetime import datetime, timedelta, time

import xlwt


class ScheduleWriter(object):
    def __init__(self, file_name: str = 'Untitled.xls', sheet_name: str = 'untitled_sheet'):
        self._file_name = file_name
        self.__book = xlwt.Workbook(file_name)
        self.__sheet = self.__book.add_sheet(sheet_name, cell_overwrite_ok=True)

        self.__day = {'Monday': 'Thứ 2',
                      'Tuesday': 'Thứ 3',
                      'Wednesday': 'Thứ 4',
                      'Thursday': 'Thứ 5',
                      'Friday': 'Thứ 6',
                      'Saturday': 'Thứ 7',
                      'Sunday': 'CN', }
        self.__started_row = 0

    def init_location(self, *args, **kwargs):
        self.__init_group(kwargs.get('location_name'), from_date=kwargs.get('from'),
                          to_date=kwargs.get('to'), start_row=self.__started_row)
        meetings = kwargs.get('meetings')
        sf_meetings = []
        for meeting in meetings:
            sf_meetings.append(self.meeting_to_dict(meeting))

        self._add_meetings(sf_meetings, self.__started_row, from_date=kwargs.get('from'))
        self.__started_row += 23
        self.__sheet.merge(self.__started_row - 1, self.__started_row - 1, 0, 30)

    def write(self, *args, **kwargs):
        pass

    def __init_group(self, location_name: str, from_date: datetime, to_date: datetime, start_row):

        date_range = (to_date - from_date).days
        # location tag
        self._add_location_name(start_row, location_name)
        self._add_date_row(start_row, date_range, from_date)
        self._add_border(start_row, date_range)
        self._add_days_in_week(start_row, date_range, from_date)

        self._add_time_frame(start_row)

    def _add_meetings(self, meetings, started_row: int, from_date: datetime):
        style1 = xlwt.XFStyle()
        style1.borders = self.__create_border()
        style1.alignment = self.__create_merge_center_alignment()
        for meeting in meetings:
            col = 2 + (meeting['started'] - from_date).days

            date = meeting['started']
            finished = meeting['finished']
            date_pivot = datetime(date.year, date.month, date.day, 8, 0, 0)

            from_row = started_row + int(2 + (date - date_pivot).seconds / 1800)
            to_row = started_row + int(1 + (finished - date_pivot).seconds / 1800)

            self.__sheet.merge(from_row, to_row, col, col)
            self.__sheet.write(from_row, col, meeting['name'], style1)
            col1 = self.__sheet.col(col)
            col1.width = 256 * len(meeting['name'])

    def _add_border(self, start_row, date_range):
        border_style = xlwt.XFStyle()
        border_style.borders = self.__create_border()

        for row in range(start_row + 2, start_row + 22):
            for col in range(2, date_range + 3):
                self.__sheet.write(row, col, '', border_style)

    def _add_location_name(self, start_row, location_name):
        tall_style = xlwt.easyxf('font:height 1440;')  # 36pt
        col1 = self.__sheet.col(0)
        col1.width = 256 * 30
        for row in range(start_row, start_row + 21):
            first_row = self.__sheet.row(row)
            first_row.set_style(tall_style)
        self.__sheet.merge(start_row, start_row + 21, 0, 0)
        style1 = xlwt.XFStyle()
        font = xlwt.Font()  # ???????
        font.name = 'Times New Roman'
        font.bold = False
        font.color_index = 0
        font.height = 300
        style1.font = font
        style1.alignment = self.__create_merge_center_alignment()

        style1.borders = self.__create_border()

        self.__sheet.write(start_row, 0, location_name, style1)

    def _add_date_row(self, start_row, date_range, from_date):
        # date
        style = xlwt.XFStyle()
        style.borders = self.__create_border()
        style.num_format_str = 'MM-YYYY'
        self.__sheet.write(start_row, 1, from_date, style)

        style.num_format_str = 'D'
        addition_days = 0
        for col in range(2, date_range + 3):
            self.__sheet.write(start_row, col, from_date + timedelta(days=addition_days), style)
            addition_days += 1

        self.__sheet.write(start_row + 1, 1, 'Giờ',
                           xlwt.easyxf("pattern: pattern solid, fore_color yellow; align: horiz right"))

    def _add_days_in_week(self, start_row: int, date_range: int, from_date: datetime):
        addition_days = 0
        style1 = xlwt.XFStyle()
        style1.borders = self.__create_border()

        for col in range(2, date_range + 3):
            date_col = from_date + timedelta(days=addition_days)
            day_of_week = self.__day[date_col.strftime('%A')]
            if day_of_week == 'CN':
                style2 = xlwt.XFStyle()
                style2.borders = self.__create_border()
                style2.pattern = self.__create_back_ground()
                for row in range(start_row + 1, start_row + 22):
                    self.__sheet.write(row, col, '', style2)
                self.__sheet.write(start_row + 1, col, day_of_week, style2)
            else:
                self.__sheet.write(start_row + 1, col, day_of_week, style1)
            addition_days += 1

    def _add_time_frame(self, start_row: int):
        col1 = self.__sheet.col(1)
        col1.width = 256 * 20

        started_time = datetime(2019, 1, 1, 8, 0, 0)
        style1 = xlwt.XFStyle()
        style1.borders = self.__create_border()
        for row in range(start_row + 2, start_row + 22):
            started_time_str = started_time.time().strftime('%Hh%M')
            next_time_str = (started_time + timedelta(minutes=30)).time().strftime('%Hh%M')
            content = started_time_str + ' - ' + next_time_str
            started_time = started_time + timedelta(minutes=30)
            self.__sheet.write(row, 1, content, style1)

    @staticmethod
    def meeting_to_dict(meeting) -> dict:
        return {
            'name': meeting.name,
            'started': meeting.started_time,
            'finished': meeting.finished_time}

    def rename(self, renamed: str):
        self._file_name = renamed + '.xls'

    def export(self, export_name: str = None):
        if export_name:
            self.rename(export_name)
        self.__book.save(self._file_name)
        # return os.path.dirname(os.path.abspath(__file__)) + '/' + self._file_name
        return self._file_name

    @staticmethod
    def __create_border():
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        return borders

    @staticmethod
    def __create_back_ground():
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
        return pattern

    @staticmethod
    def __create_merge_center_alignment():
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        return alignment
