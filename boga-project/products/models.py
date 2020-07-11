from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
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
    def timeRemaining(self):
        return self.pub_date-self.closing_time
    def timeRemainingPretty(self):
        td=(self.pub_date-self.closing_time)
        total_seconds= td.total_seconds
        hours=int(total_seconds/3600)
        minutes=int((total_seconds%3600)/60)
        return hours+":"+minutes
