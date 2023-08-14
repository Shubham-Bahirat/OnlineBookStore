from django.contrib import admin
from .models import Book,Category,Payment_Card

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","category_name")


class BookAdmin(admin.ModelAdmin):
    list_display = ("id","book_name","author_name","price","description","image","category")

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id","card_holder_name","card_number","cvv","expiry","balance")
admin.site.register(Category,CategoryAdmin) #   Register the Model in the Admin Interface
admin.site.register(Book,BookAdmin)
admin.site.register(Payment_Card,PaymentAdmin)