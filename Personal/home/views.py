from django.shortcuts import render
from finance.models import *
from django.db.models import Sum, Max, Subquery
from django.utils import timezone
from django.db.models.functions import TruncMonth, TruncDate
from customer.models import *
import json

def financeDashboard(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    net_activity = Transaction.objects.filter(date__year=current_year, date__month=current_month).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    previous_net_activity = Transaction.objects.filter(date__year=current_year, date__month=current_month -1).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    previous_total_wealth = Wallet.objects.filter(date__year=current_year, date__month=current_month-1).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_wealth = previous_total_wealth + net_activity 
    
    total_wealth_change = round((net_activity / total_wealth),3) if total_wealth !=0 else "- "
    net_activity_change = round(((net_activity - previous_net_activity) / previous_net_activity * 100),3) if previous_net_activity != 0 else "- "

    wallet_data = Wallet.objects.annotate(year_month=TruncMonth('date')).values('year_month').annotate(total_amount=Sum('amount')).order_by('year_month')
    
    evolution_period_list = []
    evolution_total_list = []
    
    if wallet_data:
            for entry in wallet_data:
                evolution_period_list.append(entry['year_month'].strftime('%Y-%m'))
                evolution_total_list.append(entry['total_amount'] or 0)


    max_date = Wallet.objects.annotate(only_date=TruncDate('date')).aggregate(max_date=Max('only_date'))['max_date']

    wallet_composition = Wallet.objects.filter(date__date=max_date).values('account__account').annotate(total_amount=Sum('amount'))
    wallet_composition = {entry['account__account']: float(entry['total_amount']) for entry in wallet_composition}

    transactions = Transaction.objects.filter(date__year=current_year, date__month=current_month)

    activities = Activity.objects.filter(sector__sector = 'finance')

    context = {
        'net_activity' : net_activity,
        'total_wealth' : total_wealth,
        'net_activity_change' : net_activity_change,
        'total_wealth_change' : total_wealth_change,
        'x_data' : evolution_period_list,
        'y_data' : evolution_total_list,
        'wallet_composition' : wallet_composition,
        'transactions' : transactions,
        'activities' : activities
    }
    return render(request, 'home/financeDashboard.html',context)


def fitnessDashboard(request):
    return render(request, 'home/fitnessDashboard.html')

def habitsDashboard(request):
    return render(request, 'home/habitsDashboard.html')

def toDoDashboard(request):
    return render(request, 'home/toDoDashboard.html')

def projectsDashboard(request):
    return render(request, 'home/projectsDashboard.html')