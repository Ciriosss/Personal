from django.db.models import Sum, F, Subquery, OuterRef
from finance.models import *

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


