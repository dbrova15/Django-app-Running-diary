from django.conf import settings
from django.db import models
from django.utils import timezone
from pytz import unicode


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now(), help_text="")
    distance = models.IntegerField(help_text="Вводить данные в метрах")
    duration = models.IntegerField(help_text="Ввидить данные в минутах")

    def publish(self):
        # self.published_date = timezone.now()
        self.save()

    def __unicode__(self):
        return unicode(self.distance)

    def __str__(self):
        return "{} {}".format(self.author, self.published_date)

    def get_data(self):
        speed = self.distance / self.duration

        return {"published_date": self.published_date,
                "distance": self.distance,
                "duration": self.duration,
                "speed": speed}
