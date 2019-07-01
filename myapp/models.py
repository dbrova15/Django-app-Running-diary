from django.conf import settings
from django.db import models
from django.utils import timezone
from pytz import unicode


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now(), help_text="")
    distance = models.IntegerField(help_text="Enter data in meters")
    duration = models.IntegerField(help_text="Enter data in minutes")
    speed = models.FloatField(default=None)

    def publish(self):
        self.save()

    def __unicode__(self):
        return unicode(self.distance)

    def __str__(self):
        return "{} {}".format(self.author, self.published_date)

    def get_data(self):
        return {"published_date": self.published_date,
                "distance": self.distance,
                "duration": self.duration,
                "speed": self.speed}

    def get_absolute_url_delete(self):
        from django.urls import reverse
        return reverse('del_data', args=[str(self.id)])

    def get_absolute_url_update(self):
        from django.urls import reverse
        return reverse('edit_data', args=[str(self.id)])
