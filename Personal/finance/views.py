from django.shortcuts import render
from .models import *

def transactions(request):
    transactions = Transaction.objects.filter(author=request.user).order_by('-date')

    context = {
        'transactions': transactions
    }
    return render(request, 'finance/transaction.html',context)

def accounts(request):
    return render(request, 'finance/account.html')

def wallet(request):
    return render(request, 'finance/wallet.html')

def investments(request):
    return render(request, 'finance/investment.html')