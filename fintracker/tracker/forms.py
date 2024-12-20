from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Budget, Debt,Savings,Transaction,Report,RecurringTransaction
import re
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Assuming you want to match phone number format like +1234567890
        if not re.match(r'^\+?\d{10,15}$', phone_number):
            raise ValidationError("Enter a valid phone number.")
        return phone_number

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ["amount", "description", "due_date", "is_paid"]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['amount', 'goal', 'description']
        widgets = {
            'goal': forms.NumberInput(attrs={'placeholder': 'Optional'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'transaction_date', 'description', 'currency']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }

class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ['transaction', 'recurrence_type', 'next_occurrence_date']
        widgets = {
            'next_occurrence_date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'type']  # Allow the user to input the report name and type

    type = forms.ChoiceField(choices=Report.TYPE_CHOICES, required=True)
