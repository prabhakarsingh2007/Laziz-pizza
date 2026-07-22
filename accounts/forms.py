from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }