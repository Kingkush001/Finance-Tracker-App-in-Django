from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Category

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'first_name', 'last_name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
