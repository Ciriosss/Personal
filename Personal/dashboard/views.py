from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from finance.models import *
import datetime



@login_required
def dashboard(request):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    net_activity = Transaction.objects.filter(author=request.user, date__year=current_year, date__month=current_month).aggregate(net_activity = Sum('amount'))['net_activity'] or 0

    context = {
        'net_activity': net_activity,
    }

    return render (request,'dashboard/dashboard.html',context)
