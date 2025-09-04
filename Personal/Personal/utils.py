from django.db.models import Sum, F, Subquery, OuterRef
from django.shortcuts import render,redirect
from dashboard.forms import *
from finance.models import *
from scipy.stats import norm


def investment_value_function(request):

    latest_date = Investment.objects.filter(author=request.user, instrument_code=OuterRef('instrument_code')).order_by('-date')

    latest_price = Subquery(latest_date.values('price')[:1])

    instrument_totals = Investment.objects.values(
    'instrument_code'
    ).annotate(
        total_quantity=Sum('quantity'),
        latest_price=latest_price
    )

    investment_value = instrument_totals.aggregate(
        total_value=Sum(F('total_quantity') * F('latest_price'))
    )['total_value']

    return investment_value

def percentage_population_function(current_wealth):
    mu = 50000
    sigma = 15000

    distribution_perc = norm.cdf(float(current_wealth), mu, sigma) * 100
    population_perc = round(100 - round(distribution_perc, 2),2)

    return population_perc

def generic_form_view(request, form_class, form_item):
    if request.method == 'POST':
        if form_item != 'Wallet':
            form = form_class(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)  
                instance.author = request.user
                instance.save()  
                return redirect('/dashboard/')
        else:
            form = WalletForm(request.user, request.POST)
            if form.is_valid():
                date = form.cleaned_data['date']
                note = form.cleaned_data['note']
                
                accounts = Account.objects.filter(author=request.user)
                
                for account in accounts:
                    amount_field = f'account_{account.id}'
                    amount = form.cleaned_data.get(amount_field, 0)
                
                    if amount:
                        Wallet.objects.create(
                            author=request.user,
                            date=date,
                            entry_date=timezone.now(),
                            account_id=account,
                            amount=amount,
                            note=note
                        )
                
                return redirect('/dashboard/')

    else:
        if form_item == 'Wallet':
            form = form_class(request.user)  # Pass user for WalletForm
        else:
            form = form_class()
        
    context = {
        'form': form,
        'form_item': form_item
    }
    
    return render(request, 'dashboard/form.html', context)

