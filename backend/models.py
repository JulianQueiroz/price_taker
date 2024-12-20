from django.db import models

# Create your models here.
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class URL(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    def __str__(self):
        return self.url

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class History(models.Model):
    id = models.AutoField(primary_key=True)
    at = models.DateTimeField(auto_now=True)
    default_price = models.DecimalField(max_digits=15, decimal_places=2)
    offer_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    offer = models.BooleanField(default=False)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"History at {self.at} - Category: {self.category}"
