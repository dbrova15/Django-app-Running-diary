import django_tables2 as tables
from .models import Post


class PersonTable(tables.Table):
    T1 = '<a class="glyphicon glyphicon-pencil" style="margin: auto; color: #d9534f; href="{{ record.get_absolute_url_update }}"></a>'
    T2 = '<a class="glyphicon glyphicon-erase" style="margin: auto; color: #d9534f; href="{{ record.get_absolute_url_delete }}"></a>'
    edit = tables.TemplateColumn(T1)
    delete = tables.TemplateColumn(T2)

    class Meta:
        model = Post
        fields = ('published_date', 'distance', 'duration', 'speed')
