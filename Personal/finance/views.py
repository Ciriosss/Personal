from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Count,Case,When
from django.db.models.functions import Abs
import datetime
import calendar
from .models import *

def transactions(request):

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    current_month_name = calendar.month_name[current_month]
    transactions = Transaction.objects.filter(author=request.user,date__year=current_year,date__month=current_month).order_by('-date')

    categories_recap = Transaction.objects.filter(author=request.user,date__year=current_year, date__month=current_month).exclude(type='Transfer').values('category_id__category').annotate(total_amount=Sum(Case(When(type='Expense', then=F('amount') * -1),
                                default=F('amount')
                    ))).annotate(count=Count('amount')).order_by(Abs('total_amount').desc())[:5]

    context = {
        'transactions': transactions,
        'current_month_name':current_month_name,
        'current_year':current_year,
        'categories_recap':categories_recap,
    }
        
    return render(request, 'finance/transaction.html',context)

def accounts(request):
    return render(request, 'finance/account.html')

def wallet(request):
    return render(request, 'finance/wallet.html')

def investments(request):
    return render(request, 'finance/investment.html')