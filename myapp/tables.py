import django_tables2 as tables
from .models import Post


class PersonTable(tables.Table):
    T1 = '<a class="glyphicon glyphicon-pencil" style="margin: auto; color: #d9534f;" href="{{ record.get_absolute_url_update }}"></a>'
    T2 = '<a class="glyphicon glyphicon-erase" style="margin: auto; color: #d9534f;" href="{{ record.get_absolute_url_delete }}"></a>'
    edit = tables.TemplateColumn(T1)
    delete = tables.TemplateColumn(T2)
    distance = tables.Column(verbose_name='Distance, m')
    duration = tables.Column(verbose_name='Duration, min')
    speed = tables.Column(verbose_name='Speed, m/h')

    class Meta:
        model = Post
        fields = ('published_date', 'distance', 'duration', 'speed')


class StatTable(tables.Table):
    week = tables.Column()
    all_records = tables.Column(verbose_name='All records')
    sum_distance = tables.Column(verbose_name='Sum distance, m')
    total_duration = tables.Column(verbose_name='Total duration, min')
    average_speed = tables.Column(verbose_name='Average speed, m/h')