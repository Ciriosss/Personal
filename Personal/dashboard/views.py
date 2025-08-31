from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from django.db.models import Sum,F
from Personal.utils import *
from finance.models import *
import datetime
import calendar

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

    current_month_name = calendar.month_name[current_month]


    ##################################
    ## Finance Dashboard card data  ##
    ##################################

    #CARD 1 : Net Activity (Transactions) this month
    net_activity = Transaction.objects.filter(author=request.user, date__year=current_year, date__month=current_month).aggregate(net_activity = Sum('amount'))['net_activity'] or 0
    budget = 500
    money_to_budget = net_activity + budget

    #CARD 2 : Change in Wealth (Wallet) this month vs last month
    prior_wealth = Wallet.objects.filter(author=request.user,date__year=prior_year, date__month=prior_month).aggregate(prior_wealth = Sum('amount'))['prior_wealth'] or 0
    current_wealth = prior_wealth + net_activity
    change_prc = round(((current_wealth - prior_wealth) / prior_wealth * 100) if prior_wealth != 0 else 0,0)

    #CARD 3 : INVESTMENT PROFIT/LOSS (Investments)
    investment_cost = Investment.objects.filter(author=request.user).aggregate(investment_cost=Sum(F('price') * F('quantity')))['investment_cost'] or 0
    investment_value = investment_value_function(request) or 0

    investment_profit = investment_value-investment_cost
    investment_profit_prc = round(investment_profit / investment_cost * 100,2) if investment_cost !=0 else 0

    #CARD 4 : TOP % OF POPULATION
    population_perc = percentage_population_function(current_wealth)

    ##################################
    ##     Finance data             ##
    ##################################

    #WEALTH EVOLUTION
    wallet_data = Wallet.objects.filter(author=request.user).annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')

    #WALLET COMPOSITION
    wallet_composition = Wallet.objects.filter(author=request.user,date__year=current_year, date__month=current_month).values(asset_class = F('account_id__account_class__asset_class_name')).annotate(total_amount=Sum('amount')).order_by('account_id__account_class__asset_class_name')

    context = {
        'current_month_name':current_month_name,
        'current_year':current_year,
        'net_activity': net_activity, 
        'current_wealth': current_wealth,
        'money_to_budget':money_to_budget,
        'change_prc':change_prc,
        'investment_cost': investment_cost,
        'investment_profit':investment_profit,
        'investment_profit_prc':investment_profit_prc,
        'population_perc':population_perc,
        'wallet_data':wallet_data,
        'wallet_composition':wallet_composition
    }

    return render (request,'dashboard/dashboard.html',context)