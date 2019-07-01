from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from pytz import unicode


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True, default=get_current_timezone(), help_text="")
    distance = models.IntegerField(help_text="Вводить данные в метрах")
    duration = models.IntegerField(help_text="Вводить данные в минутах")
    speed = models.FloatField(default=None)

    def publish(self):
        # self.speed = self.distance / self.duration
        # self.published_date = timezone.now()
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
        # from django.core.urlresolvers import reverse
        return reverse('del_post', args=[str(self.id)])

    def get_absolute_url_update(self):
        from django.urls import reverse
        return reverse('edit_post', args=[str(self.id)])
