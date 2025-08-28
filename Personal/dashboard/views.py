from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Mult
from finance.models import *
import datetime

@login_required
def dashboard(request):

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    if current_month == 1:
        prior_month = 12
        prior_year = current_year - 1
    else:
        prior_month = current_month - 1
        prior_year = current_year

    net_activity = Transaction.objects.filter(author=request.user, date__year=current_year, date__month=current_month).aggregate(net_activity = Sum('amount'))['net_activity'] or 0
    budget = 500
    money_to_budget = net_activity + budget
    
    prior_wealth = Wallet.objects.filter(author=request.user,date__year=prior_year, date__month=prior_month).aggregate(prior_wealth = Sum('amount'))['prior_wealth'] or 0
    current_wealth = (Wallet.objects.filter(author=request.user,date__year=current_year, date__month=current_month).aggregate(current_wealth = Sum('amount'))['current_wealth'] or 0) + net_activity
    change_prc = round(((current_wealth - prior_wealth) / prior_wealth * 100) if prior_wealth != 0 else 0,0)

  
    context = {
        'net_activity': net_activity, 
        'current_wealth': current_wealth,
        'money_to_budget':money_to_budget,
        'change_prc':change_prc
    }

    return render (request,'dashboard/dashboard.html',context)
