from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    pub_date=models.DateTimeField(auto_now_add=True)
    closing_time=models.DateTimeField(default=datetime.now())
    orders=models.IntegerField(default=1)
    image=models.ImageField(upload_to="images/")
    body=models.TextField()
    customers=models.ManyToManyField(User)

    def __str__(self):
        return self.title
    def timerOver(self):
        if timezone.now()>=self.closing_time:
            return True
    def timeRemainingPretty(self):
        td=self.closing_time-timezone.now()
        minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
        hours, minutes = divmod(minutes, 60)
        return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
