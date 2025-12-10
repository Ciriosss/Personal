from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Count,Case,When
from django.db.models.functions import Abs
import datetime
import calendar
from .models import *

@login_required
def transactions(request):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    current_month_name = calendar.month_name[current_month]
    transactions = Transaction.objects.filter(author=request.user,date__year=current_year,date__month=current_month).order_by('-date')

    categories_recap = transactions.exclude(type='Transfer').values('category_id__category').annotate(total_amount=Sum(Case(When(type='Expense', then=F('amount') * -1),
                                default=F('amount')
                    ))).annotate(count=Count('amount')).order_by(Abs('total_amount').desc())
    
    labels_recap = transactions.exclude(type='Transfer').values('label_id__label').annotate(total_amount=Sum(Case(When(type='Expense', then=F('amount') * -1),
                                default=F('amount')
                    ))).annotate(count=Count('amount')).order_by(Abs('total_amount').desc())

    transaction_count = transactions.count()

    context = {
        'transactions': transactions,
        'current_month_name':current_month_name,
        'current_year':current_year,
        'categories_recap':categories_recap,
        'transaction_count':transaction_count,
        'labels_recap':labels_recap
    }
        
    return render(request, 'finance/transaction.html',context)

@login_required
def accounts(request):

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    current_month_name = calendar.month_name[current_month]
    transactions = Transaction.objects.filter(author=request.user,date__year=current_year,date__month=current_month).order_by('-date')

    accounts_recap = transactions.exclude(type='Transfer').values('account_id','account_id__account_class__asset_class_name','account_id__account_name','account_id__status').annotate(total_amount=Sum(Case(When(type='Expense', then=F('amount') * -1),
                                default=F('amount')
                    ))).annotate(count=Count('amount')).order_by(Abs('total_amount').desc())
    
    accounts_count = accounts_recap.count()
    
    context = {
        'transactions': transactions,
        'current_month_name':current_month_name,
        'current_year':current_year,
        'accounts_recap':accounts_recap,
        'accounts_count':accounts_count
    }
    return render(request, 'finance/account.html',context)

def wallet(request):
    return render(request, 'finance/wallet.html')

def investments(request):
    return render(request, 'finance/investment.html')