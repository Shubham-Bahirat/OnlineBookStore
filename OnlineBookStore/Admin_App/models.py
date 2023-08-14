from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=80)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "Category"


class Book(models.Model):
    book_name = models.CharField(max_length=60)
    author_name = models.CharField(max_length=60)
    price = models.FloatField(default=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images",default="abc.jpg")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        db_table = "Book"

class Payment_Card(models.Model):
    card_holder_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=5)
    expiry = models.CharField(max_length=12)
    balance = models.FloatField()

    class Meta:
        db_table = "Payment_Card"