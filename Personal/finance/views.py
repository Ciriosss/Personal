from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Max
from django.utils import timezone
from django.db.models.functions import TruncDate
from .models import *
from .forms import TransactionForm


@login_required
def transactions(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    transactions = Transaction.objects.filter(date__year=current_year, date__month=current_month)
    account_pivot = Transaction.objects.filter(date__year=current_year, date__month=current_month).values(
        'category__category'
    ).annotate(total_amount=Sum('amount'))
    account_pivot = {entry['category__category']: float(entry['total_amount']) for entry in account_pivot}

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.author = request.user
            transaction.save()
            return redirect('fin-transactions')
    else:
        form = TransactionForm()

    context = {
        'transactions': transactions,
        'now': now,
        'account_pivot': account_pivot,
        'form': form
    }

    return render(request, 'finance/transactions.html', context)

@login_required
def wallet(request):

    composition_by_date = (
        Wallet.objects
        .annotate(date_only=TruncDate('date'))
        .values('date_only', 'account__type__type')
        .annotate(total_amount=Sum('amount'))
        .order_by('date_only')
    )
    composition_by_date = [
            {
                'date': item['date_only'].isoformat(),
                'account__type__name': item['account__type__type'],
                'total_amount': item['total_amount']
            }
            for item in composition_by_date
        ]
    

    wallet_pivot = (
    Wallet.objects
    .annotate(only_date=TruncDate('date'))
    .values('only_date')
    .annotate(total_amount=Sum('amount'))
    .order_by('only_date'))

    wallet_evolution = {
        item['only_date'].isoformat(): item['total_amount'] 
        for item in wallet_pivot
    }

    max_date = Wallet.objects.annotate(only_date=TruncDate('date')).aggregate(max_date=Max('only_date'))['max_date']
    wallet_composition = Wallet.objects.filter(date__date=max_date).values('account__account').annotate(total_amount=Sum('amount'))
    wallet_composition = {entry['account__account']: float(entry['total_amount']) for entry in wallet_composition}
    wallet_data = Wallet.objects.filter(date__date=max_date)

    context = {
       'wallet_evolution' : wallet_evolution,
       'composition_by_date' : composition_by_date,
       'wallet_composition' : wallet_composition,
       'wallet_data' : wallet_data,
       'max_date' : max_date
    }

    return render(request, 'finance/wallet.html',context)

def investments(request):

    investments_detail = Investment.objects.all()

    context = {
        'investments_detail' : investments_detail,
    }


    return render(request, 'finance/investments.html', context)


def check(request):
    return render(request, 'finance/check.html')

    
def accounts(request):
    return render(request, 'finance/accounts.html')



 
