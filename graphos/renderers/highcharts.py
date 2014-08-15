from .base import BaseChart
import json
from time import mktime

from django.template.loader import render_to_string

class BaseHighCharts(BaseChart):
    def get_template(self):
        return "graphos/highcharts.html"

    def get_series(self):
        data = self.get_data()
        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+1)[1:]})
        return json.dumps(serieses)

    def get_categories(self):
        return json.dumps(column(self.get_data(), 0)[1:])

    def get_x_axis_title(self):
        if self.context_data.has_key('x_axis_title'):
            return self.context_data['x_axis_title']
        return self.get_data()[0][0]


class DateTimeLineChart(BaseHighCharts):

    def get_chart_type(self):
        return "line"

    def get_categories(self):
        return None

    def get_series(self):
        tmpdata = self.get_data()

        tzoffset = self.get_tzoffset()

        data=[tmpdata[0]]
        for d in tmpdata[1:]:
            data.append([datetime_to_timestamp(d[0]) + tzoffset * 1000 , d[1] ])

        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": data[1:]})
        return json.dumps(serieses)
    
    def get_x_axis_datetime_format(self, formats=None):
        
        x_axis_format = {
            'millisecond': '%H:%M:%S.%L',
            'second': '%H:%M:%S',
            'minute': '%H:%M',
            'hour': '%H:%M',
            'day': '%e. %b',
            'week': '%e. %b',
            'month': '%b \'%y',
            'year': '%Y'
        }
        if formats is not None:
            x_axis_format = formats
        return json.dumps(x_axis_format)

    def get_x_axis_type(self):
        return 'datetime'

    def get_tzoffset(self):
        try:
            return self.context_data['tzoffset']
        except:
            return 0

class LineChart(BaseHighCharts):
    def get_chart_type(self):
        return "line"


class BarChart(BaseHighCharts):
    def get_chart_type(self):
        return "bar"


class ColumnChart(BaseHighCharts):
    def get_chart_type(self):
        return "column"


class PieChart(BaseHighCharts):
    def get_chart_type(self):
        return "pie"


def column(matrix, i):
    return [row[i] for row in matrix]


def datetime_to_timestamp(dt):
    return int(mktime(dt.timetuple())*1000)
