import datetime

from django.db.models import Avg, F
from django.db.models.functions import ExtractWeek

from myapp.models import Post

today = datetime.datetime.now()
last_year = today.year - 1

# data_set = Post.objects.filter(published_date__gt=last_year).annotate(
#     week=ExtractWeek('date')
# ).values('week').annotate(
#     week_total=Avg(F('total'))
# ).order_by('week')

data_set = Post.objects.filter(published_date__gt=last_year).annotate(week=ExtractWeek('date')).values('week')
print(data_set)