from django.db import models
from menu.models import Category

# Create your models here.

class PopularItem(models.Model):
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='popular/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='popular_items')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
