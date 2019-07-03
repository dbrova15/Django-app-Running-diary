from django.conf import settings
from django.db import models
from django.utils import timezone
from django.views.generic import UpdateView
from pytz import unicode
from django.urls import reverse


class Add_data(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, default=timezone.now(), help_text="")
    distance = models.IntegerField(help_text="Enter data in meters")
    duration = models.IntegerField(help_text="Enter data in minutes")
    speed = models.FloatField(default=None)

    def __unicode__(self):
        return unicode(self.distance)

    def __str__(self):
        return "{} {}".format(self.author, self.date_time)

    # def get_data(self):
    #     return {"date_time": self.date_time,
    #             "distance": self.distance,
    #             "duration": self.duration,
    #             "speed": self.speed}

    def get_absolute_url_delete(self):
        return reverse('del_data', args=[str(self.id)])

    def get_absolute_url_update(self):
        return reverse('edit_data', args=[str(self.id)])
