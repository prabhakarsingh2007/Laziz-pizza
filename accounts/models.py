from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Hash password if it is not already hashed
        if self.password:
            try:
                identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.address_text[:30]}"