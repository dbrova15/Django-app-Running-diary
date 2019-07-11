from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Add_data(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, default=timezone.now(), help_text="")
    distance = models.IntegerField(help_text="Enter data in meters", default=1)
    duration = models.IntegerField(help_text="Enter data in minutes", default=1)
    speed = models.FloatField(default=None)

    def __unicode__(self):
        return self.distance

    def __str__(self):
        return "{} {}".format(self.author, self.date_time)

    def get_absolute_url_delete(self):
        return reverse('del_data', args=[str(self.id)])

    def get_absolute_url_update(self):
        return reverse('edit_data', args=[str(self.id)])
