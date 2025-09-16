from django.shortcuts import render

def transactions(request):
    return render(request, 'finance/transaction.html')

def accounts(request):
    return render(request, 'finance/account.html')

def wallet(request):
    return render(request, 'finance/wallet.html')

def investments(request):
    return render(request, 'finance/investment.html')