from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    FOOD_TYPE = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE, default='Veg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food/')
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name