from django.db import models
from Admin_App.models import Book
from datetime import datetime
from datetime import datetime, date, timedelta

# Create your models here.
def dt():
    td = datetime.today()
    delivery = td + timedelta(days=4)
    return delivery

class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=15)
    address = models.CharField(max_length=350)

    class Meta:
        db_table = "UserInfo"

class MyCart(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    qty = models.IntegerField()

class orderInfo(models.Model):
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    order_date = models.DateField(default = datetime.now )  
    delivery_date = models.DateField(default = dt() )
    amount = models.FloatField(default=1200)
    details = models.CharField(max_length=600)

    class Meta:
        db_table = "orderInfo"


class ContactInfo(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(default=1)
    message = models.CharField(max_length=600)

    class Meta:
        db_table = "ContactInfo"
