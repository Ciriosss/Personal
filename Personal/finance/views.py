from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime
import calendar
from .models import *

def transactions(request):

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    user = request.user

    if current_month == 1:
        prior_month = 12
        prior_year = current_year - 1
    else:
        prior_month = current_month - 1
        prior_year = current_year

    current_month_name = calendar.month_name[current_month]
    transactions = Transaction.objects.filter(author=request.user,date__year=current_year, 
                    date__month=current_month).order_by('-date')

    context = {
        'transactions': transactions,
        'current_month_name':current_month_name,
        'current_year':current_year,
    }
    return render(request, 'finance/transaction.html',context)

def accounts(request):
    return render(request, 'finance/account.html')

def wallet(request):
    return render(request, 'finance/wallet.html')

def investments(request):
    return render(request, 'finance/investment.html')