from .base import BaseChart
import json
from calendar import timegm

from django.template.loader import render_to_string
from django.utils import timezone
import datetime

import json

class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = timezone.localtime(o).strftime("%Y-%m-%dT%H:%M:%S")
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)



class BaseDimpleJS(BaseChart):

    def process_data(self):
        return True

    def get_data(self):

        tmpdata = self.data_source.data 
        data = []
        fields = tmpdata[0]

        for d in tmpdata[1:]:
            row = {}
            for i, v in enumerate(d):
                row[fields[i]] = v
            data.append(row)

        self.data = data



    def get_data_json(self):

        if not hasattr(self, 'data'):
            self.get_data()
        print self.data
        return json.dumps(self.data, cls=DjangoJSONEncoder)

    def get_series(self):
        data = self.get_data()
        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            serieses.append({'name': name, 'data': column(data, i+1)[1:]})
        return json.dumps(serieses)

    def get_chart_type(self):
        try:
            return self.context_data['chart_type']
        except:
            return "line"

    def get_categories(self):
        return json.dumps(column(self.get_data(), 0)[1:])

    def get_x_axis_title(self):
        try:
            return self.context_data['x_axis_title']
        except:
            return self.get_data()[0][0]

    def get_y_axis_title(self):
        try:
            return self.context_data['y_axis_title']
        except:
            return self.get_data()[0][1]

    def get_x_axis_field(self):
        try:
            return self.context_data['x_axis_field']
        except:
            return self.data_source.fields[0]

    def get_y_axis_field(self):
        try:
            return self.context_data['y_axis_field']
        except:
            return self.data_source.fields[1]

    def get_x_axis_field_js(self):
        
        try:
            return self.context_data['x_axis_field_js']
        except:
            return self.data_source.fields[0]

    def get_y_axis_field_js(self):
        try:
            return self.context_data['y_axis_field_js']
        except:
            return self.data_source.fields[1]


class DateTimeChart(BaseDimpleJS):
    def get_template(self):
        return "graphos/dimplejs/datetime.html"

    def get_x_axis_type(self):
        return 'datetime'

class PieChart(BaseDimpleJS):
    def get_template(self):
        return "graphos/dimplejs/pie.html"

    def get_chart_type(self):
        return "pie"

class CategoryChart(BaseDimpleJS):
    """docstring for CaategoryChart"""
    def get_template(self):
        return "graphos/dimplejs/category.html"

    def get_chart_type(self):
        return "bar"

class LineChart(BaseDimpleJS):
    def get_chart_type(self):
        return "line"


class BarChart(BaseDimpleJS):
    def get_chart_type(self):
        return "bar"


class ColumnChart(BaseDimpleJS):
    def get_chart_type(self):
        return "column"


def column(matrix, i):
    return [row[i] for row in matrix]


def datetime_to_timestamp(dt):
    return timegm(dt.timetuple())
