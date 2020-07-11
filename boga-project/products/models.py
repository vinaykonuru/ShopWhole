from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    pub_date=models.DateTimeField(auto_now_add=True)
    orders=models.IntegerField(default=0)
    image=models.ImageField(upload_to="images/")
    body=models.TextField()
    customers=models.ManyToManyField(User)

    def __str__(self):
        return self.title
