from django.db import models


class FoodItem(models.Model):
    CATEGORY = [
        ('Pizza', 'Pizza'),
        ('Burger', 'Burger'),
        ('Pasta', 'Pasta'),
        ('Drinks', 'Drinks'),
        ('Dessert', 'Dessert'),
        ('Combo', 'Combo'),
    ]

    FOOD_TYPE = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE, default='Veg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food/')
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name