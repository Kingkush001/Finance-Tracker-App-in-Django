from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm,DebtForm,BudgetForm,CategoryForm,SavingsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Category,Budget,Debt,Savings,Report
from django.contrib.auth import get_user_model
import csv
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
import io
User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user after validation
            user = form.save()
            # You can add custom logic here if needed, e.g., send confirmation email

            # Display success message
            messages.success(request, "Account created successfully! Please login.")
            return redirect('tracker:login')  # Redirect to the login page
        else:
            # If the form is invalid, display error messages
            messages.error(request, "Error during registration. Please try again.")
    else:
        # If the request is GET, create an empty form
        form = CustomUserCreationForm()

    # Render the registration template with the form
    return render(request, 'tracker/register.html', {'form': form})


# Login View
def user_login(request):
    if request.method == 'POST':
        # Create the AuthenticationForm instance with POST data
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('tracker:dashboard')  # Redirect to the dashboard
            else:
                # If authentication fails, provide an error message
                messages.error(request, "Invalid username or password.")
        else:
            # If the form is not valid, show general error message
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()

    return render(request, 'tracker/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('tracker:login')  # Redirect to the login page after logout


# Dashboard View (Only accessible after login)
@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'tracker/category_list.html', {'categories': categories})

# Create view for categories
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save the form instance without committing to the database
            category = form.save(commit=False)
            # Assign the currently logged-in user to the category
            category.user_id = request.user.id
            # Save the instance to the database
            category.save()
            return redirect('tracker:category_list')
    else:
        form = CategoryForm()
    return render(request, 'tracker/category_form.html', {'form': form})



# Update view for categories
@login_required
def category_update(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('tracker:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'tracker/category_form.html', {'form': form})

# Delete view for categories
@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('tracker:category_list')
    return render(request, 'tracker/category_confirm_delete.html', {'category': category})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'tracker/budget_list.html', {'budgets': budgets})

@login_required
def budget_detail(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    return render(request, 'tracker/budget_detail.html', {'budget': budget})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('tracker:budget_list')
    else:
        form = BudgetForm()
    return render(request, 'tracker/budget_form.html', {'form': form})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('tracker:budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'tracker/budget_form.html', {'form': form})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('tracker:budget_list')
    return render(request, 'tracker/budget_confirm_delete.html', {'budget': budget})


@login_required
def debt_list(request):
    debts = Debt.objects.filter(user=request.user)
    return render(request, "tracker/debt_list.html", {"debts": debts})

@login_required
def debt_detail(request, debt_id):
    debt = get_object_or_404(Debt, pk=debt_id, user=request.user)
    return render(request, "tracker/debt_detail.html", {"debt": debt})

@login_required
def debt_create(request):
    if request.method == "POST":
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user
            debt.save()
            return redirect("tracker:debt_list")
    else:
        form = DebtForm()
    return render(request, "tracker/debt_form.html", {"form": form})

@login_required
def debt_update(request, debt_id):
    debt = get_object_or_404(Debt, pk=debt_id, user=request.user)
    if request.method == "POST":
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            return redirect("tracker:debt_list")
    else:
        form = DebtForm(instance=debt)
    return render(request, "tracker/debt_form.html", {"form": form})

@login_required
def debt_delete(request, debt_id):
    debt = get_object_or_404(Debt, pk=debt_id, user=request.user)
    if request.method == "POST":
        debt.delete()
        return redirect("tracker:debt_list")
    return render(request, "tracker/debt_confirm_delete.html", {"debt": debt})


# Display all savings
@login_required
def savings_list(request):
    savings = Savings.objects.filter(user=request.user)
    return render(request, 'tracker/savings_list.html', {'savings': savings})

# Create a new savings entry
@login_required
def savings_create(request):
    if request.method == "POST":
        form = SavingsForm(request.POST)
        if form.is_valid():
            savings = form.save(commit=False)
            savings.user = request.user
            savings.save()
            return redirect('tracker:savings_list')
    else:
        form = SavingsForm()
    return render(request, 'tracker/savings_form.html', {'form': form})

# Update an existing savings entry
@login_required
def savings_update(request, savings_id):
    savings = get_object_or_404(Savings, savings_id=savings_id, user=request.user)
    if request.method == "POST":
        form = SavingsForm(request.POST, instance=savings)
        if form.is_valid():
            form.save()
            return redirect('tracker:savings_list')
    else:
        form = SavingsForm(instance=savings)
    return render(request, 'tracker/savings_form.html', {'form': form})

# Delete a savings entry
@login_required
def savings_delete(request, savings_id):
    savings = get_object_or_404(Savings, savings_id=savings_id, user=request.user)
    if request.method == "POST":
        savings.delete()
        return redirect('tracker:savings_list')
    return render(request, 'tracker:/savings_confirm_delete.html', {'savings': savings})


# View to list reports
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'tracker/report_list.html', {'reports': reports})

from datetime import datetime
from .models import Report
from django.utils import timezone

def generate_report(user, report_name, report_type):
    # Check if the report type is valid
    valid_report_types = ['summary', 'detailed', 'monthly', 'annual']
    if report_type not in valid_report_types:
        raise ValueError("Invalid report type")

    # Create a new report
    new_report = Report.objects.create(
        user=user,
        name=report_name,
        type=report_type,
        generated_at=timezone.now(),  # Timestamp when the report is generated
        created_at=timezone.now(),  # Timestamp when the report is created
        updated_at=timezone.now()  # Timestamp when the report is updated
    )

    return new_report

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReportForm
from .models import Report
  # assuming your function is in a utils.py file

def generate_report_view(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            report_name = form.cleaned_data['name']
            report_type = form.cleaned_data['type']
            
            try:
                # Generate the report
                report = generate_report(request.user, report_name, report_type)
                messages.success(request, f"Report '{report.name}' generated successfully.")
                return redirect('report_detail', report_id=report.report_id)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ReportForm()

    return render(request, 'generate_report.html', {'form': form})


# View to download the report as CSV
def download_report_csv(request, report_id):
    report = Report.objects.get(report_id=report_id)

    # Create HTTP response for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report.name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Report ID', 'User', 'Name', 'Type', 'Generated At', 'Created At', 'Updated At'])
    writer.writerow([report.report_id, report.user.username, report.name, report.get_type_display(),
                     report.generated_at, report.created_at, report.updated_at])

    return response

# View to download the report as PDF
def download_report_pdf(request, report_id):
    report = Report.objects.get(report_id=report_id)

    # Create HTTP response for PDF download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report.name}.pdf"'

    # Create the PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Report ID: {report.report_id}")
    p.drawString(100, 730, f"User: {report.user.username}")
    p.drawString(100, 710, f"Name: {report.name}")
    p.drawString(100, 690, f"Type: {report.get_type_display()}")
    p.drawString(100, 670, f"Generated At: {report.generated_at}")
    p.drawString(100, 650, f"Created At: {report.created_at}")
    p.drawString(100, 630, f"Updated At: {report.updated_at}")
    p.showPage()
    p.save()

    # Return PDF response
    response.write(buffer.getvalue())
    buffer.close()
    return response


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Currency
import csv

# List all currencies
def currency_list(request):
    currencies = Currency.objects.all()
    return render(request, 'tracker/currency_list.html', {'currencies': currencies})

# Currency detail view
def currency_detail(request, currency_id):
    currency = get_object_or_404(Currency, pk=currency_id)
    return render(request, 'tracker/currency_detail.html', {'currency': currency})

# Add a new currency
def add_currency(request):
    if request.method == 'POST':
        currency_code = request.POST.get('currency_code')
        exchange_rate = request.POST.get('exchange_rate')
        Currency.objects.create(currency_code=currency_code, exchange_rate=exchange_rate)
        return redirect('tracker:currency_list')
    return render(request, 'tracker/add_currency.html')

# Download currencies as CSV
def download_currencies_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="currencies.csv"'

    writer = csv.writer(response)
    writer.writerow(['Currency ID', 'Currency Code', 'Exchange Rate'])

    for currency in Currency.objects.all():
        writer.writerow([currency.currency_id, currency.currency_code, currency.exchange_rate])

    return response

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Transaction, Category, Currency
from .forms import TransactionForm

def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)  # Don't save yet
            transaction.user = request.user       # Assign the user
            transaction.save()                    # Save with the user assigned
            return redirect(reverse('tracker:transaction_list'))
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form})


def transaction_edit(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect(reverse('tracker:transaction_list'))
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'tracker/transaction_form.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import RecurringTransaction
from .forms import RecurringTransactionForm

# List View
def recurring_list(request):
    recurring_transactions = RecurringTransaction.objects.all()
    return render(request, 'tracker/recurring_list.html', {'recurring_transactions': recurring_transactions})

# Create View
def recurring_create(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('tracker:recurring_list'))
    else:
        form = RecurringTransactionForm()
    return render(request, 'tracker/recurring_form.html', {'form': form})

# Update View
def recurring_edit(request, recurring_id):
    recurring_transaction = get_object_or_404(RecurringTransaction, recurring_id=recurring_id)
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST, instance=recurring_transaction)
        if form.is_valid():
            form.save()
            return redirect(reverse('tracker:recurring_list'))
    else:
        form = RecurringTransactionForm(instance=recurring_transaction)
    return render(request, 'tracker/recurring_form.html', {'form': form})

# Delete View
def recurring_delete(request, recurring_id):
    recurring_transaction = get_object_or_404(RecurringTransaction, recurring_id=recurring_id)
    if request.method == 'POST':
        recurring_transaction.delete()
        return redirect(reverse('tracker:recurring_list'))
    return render(request, 'tracker/recurring_confirm_delete.html', {'recurring_transaction': recurring_transaction})


