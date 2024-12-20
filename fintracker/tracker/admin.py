from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Category,Budget, Debt,Currency,Transaction,RecurringTransaction

class CustomUserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('email', 'phone', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    
    # Fields to use in the add/edit user forms in the admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('date_joined', 'last_login')  # Make 'date_joined' and 'last_login' read-only

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    filter_horizontal = ()

# Register the CustomUser model with the custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)


# Optionally, customize the admin display
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name', 'description', 'created_at', 'updated_at')  # Fields to display in list view
    search_fields = ('name',)  # Add a search bar for 'name'
    list_filter = ('created_at',)  # Filter by creation date

# Register the model with the admin
admin.site.register(Category, CategoryAdmin)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('budget_id', 'user', 'category', 'amount', 'start_date', 'end_date', 'created_at')
    search_fields = ('user__username', 'category__name')
    list_filter = ('start_date', 'end_date')


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ("debt_id", "user", "amount", "due_date", "is_paid", "created_at", "updated_at")
    list_filter = ("is_paid", "due_date")
    search_fields = ("user__username", "description")
    ordering = ("-created_at",)
    date_hierarchy = "due_date"

    # Optional: Custom admin features for better usability
    fieldsets = (
        ("Basic Information", {
            "fields": ("user", "amount", "description", "due_date", "is_paid")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_id', 'currency_code', 'exchange_rate')  # Fields to display in admin
    search_fields = ('currency_code',)  # Add search functionality for currency codes

admin.site.register(Transaction)

@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ('recurring_id', 'transaction', 'recurrence_type', 'next_occurrence_date', 'created_at')
    list_filter = ('recurrence_type',)
    search_fields = ('transaction__description',)
