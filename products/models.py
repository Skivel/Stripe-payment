from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name="Назва пакету", max_length=100)
    price = models.IntegerField(verbose_name="Ціна", default=0)  # cents
    vote = models.IntegerField(verbose_name="Кількість голосів", default=0)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)