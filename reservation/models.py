from django.db import models
from accounts.models import User


class Reservation(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_request = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name