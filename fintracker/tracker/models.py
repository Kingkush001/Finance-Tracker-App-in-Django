from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User 
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User 
 

User = get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, first_name, last_name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, first_name, last_name, password=None):
        user = self.create_user(email, phone, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Related fields with unique related_name to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique related_name
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        """Return True if the user has the specified permission."""
        return True

    def has_module_perms(self, app_label):
        """Return True if the user has permissions to view the app `app_label`."""
        return True


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.name
    
class Budget(models.Model):
    budget_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')  # ForeignKey to User
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='budgets')  # ForeignKey to Category
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Budgeted amount
    start_date = models.DateField()  # Start date of the budget
    end_date = models.DateField()  # End date of the budget
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"{self.user.username} - {self.category.name}: {self.amount}"


class Debt(models.Model):
    debt_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="debt")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Debt {self.debt_id} - User {self.user.username} - Amount {self.amount}"


class Savings(models.Model):
    savings_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="savings")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Savings {self.savings_id} - User {self.user_id}"

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to the User model
    name = models.CharField(max_length=255)  # Name of the report
    TYPE_CHOICES = [
        ('summary', 'Summary'),
        ('detailed', 'Detailed'),
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # Report type (summary, detailed, monthly, annual)
    generated_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the report was generated
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the report was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the report was last updated

    def __str__(self):
        return self.name  # Return the report name as a string representation

class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)  # Automatically increments for each new entry
    currency_code = models.CharField(max_length=10, unique=True)  # E.g., USD, EUR
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)  # Exchange rate to a base currency

    def __str__(self):
        return f"{self.currency_code} ({self.exchange_rate})"

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="transactions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.user.username}"
    
class RecurringTransaction(models.Model):
    RECURRING_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    recurring_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='recurring_transactions')
    recurrence_type = models.CharField(max_length=10, choices=RECURRING_TYPES)
    next_occurrence_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recurring {self.recurrence_type} for {self.transaction}"
