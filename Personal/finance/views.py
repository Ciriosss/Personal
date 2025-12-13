from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Count,Case,When,Window,Value
from django.db.models.functions import Abs
from django.db.models.functions import TruncDate
from django.db import connections
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

@login_required
def investments(request):
    investments_list = Investment.objects.filter(author=request.user).order_by('-date')
    investments = Investment.objects.filter(author=request.user)
    investments_count = investments.count()

    investment_summary_query = """
                WITH investments AS (
                                
                            SELECT 
                                id,
                                author_id,
                                instrument_code_id,
                                date,
                                price,
                                quantity,
                                price * quantity AS invested,
                                SUM(quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date) AS cum_quantity,
                                SUM(price * quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date) AS cum_invested,
                                IIF(
                                    quantity < 0,
                                    ROUND(
                                        (price * SUM(quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date))
                                        - SUM(price * quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date)
                                    ,2)
                                ,0) AS adjustment,
                                IIF(quantity >= 0, 'Buy', 'Sell') AS operation
                            FROM 
                                finance_investment
                            WHERE 
                                author_id = %s
                            ORDER BY 
                                author_id,
                                instrument_code_id,
                                date
            ),
                            drill_down_adjustment AS (
                                SELECT
                                    id, 
                                    author_id,
                                    instrument_code_id,
                                    date,
                                    price,
                                    quantity,
                                    invested,
                                    cum_quantity,
                                    cum_invested,
                                    IIF(
                                adjustment = 0 
                                AND LAG(adjustment) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date) <> 0,
                                LAG(adjustment) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date),
                                adjustment
                            ) AS adjustment,
                                    operation
                                FROM
                                    investments
                            ),
                            investments_adj AS(
                                SELECT
                                    id, 
                                    author_id,
                                    instrument_code_id,
                                    date,
                                    price,
                                    quantity,
                                    invested,
                                    cum_quantity,
                                    cum_invested  
                                    + COALESCE(LAG(adjustment) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date),0)
                                    AS cum_invested,
                                    adjustment,
                                    operation
                                FROM
                                    drill_down_adjustment
                            ),
                            investments_recalculation AS (
                                SELECT
                                    id, 
                                    author_id,
                                    instrument_code_id,
                                    date,
                                    price,
                                    quantity,
                                    invested,
                                    cum_quantity,
                                    cum_invested ,
                                    operation,
                                    IIF(operation = 'Buy',ROUND((price * cum_quantity) - cum_invested,2),0)  as urgl,
                                    IIF(operation = 'Sell',ROUND((price * cum_quantity) - cum_invested,2),0) as rgl
                                FROM investments_adj
                            ),
                            datamart AS (
                        SELECT 
                                Investment.*,
                                Instrument.instrument_code AS instrument_code,
                                Instrument.instrument_name AS instrument_name
                        FROM investments_recalculation Investment
                        LEFT JOIN finance_instrument instrument
                        ON 1 = 1
                            AND Investment.instrument_code_id = instrument.id),
                        RGL AS (
                            SELECT 
                                instrument_code_id,
                                instrument_code,
                                instrument_name,
                                SUM(RGL) AS RGL,
                                COUNT(RGL) AS investment_count
                            FROM datamart
                            GROUP BY 
                                instrument_code_id,
                                instrument_code,
                                instrument_name
                            
                        ),
                        URGL AS (
                            SELECT 
                                dt.instrument_code_id,
                                dt.instrument_code,
                                dt.instrument_name,
                                dt.URGL
                                
                            FROM datamart dt
                            JOIN (
                                SELECT 
                                    instrument_code_id,
                                    instrument_code,
                                    instrument_name,
                                    MAX(Date) AS last_date
                                FROM datamart
                                GROUP BY 
                                    instrument_code_id,
                                    instrument_code,
                                    instrument_name) AS last_date
                            ON 1 = 1
                                AND dt.instrument_code_id = last_date.instrument_code_id
                                AND dt.date = last_date.last_date
                        )
            SELECT 
                RGL.instrument_code_id,
                RGL.instrument_code,
                RGL.instrument_name,
                investment_count,
                URGL,
                RGL

            FROM RGL
            FULL OUTER JOIN URGL
            ON RGL.instrument_code_id = URGL.instrument_code_id
""" % (request.user.id)

    investment_evolution_query = """ 
            WITH investments AS (
                    
                SELECT 
                    id,
                    author_id,
                    instrument_code_id,
                    DATE(date) AS date,
                    price,
                    quantity,
                    price * quantity AS invested,
                    SUM(quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date) AS cum_quantity,
                    SUM(price * quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date) AS cum_invested,
                    IIF(
                        quantity < 0,
                        ROUND(
                            (price * SUM(quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date))
                            - SUM(price * quantity) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date)
                        ,2)
                    ,0) AS adjustment,
                    IIF(quantity >= 0, 'Buy', 'Sell') AS operation
                FROM 
                    finance_investment
                WHERE 
                    author_id = %s
                ORDER BY 
                    author_id,
                    instrument_code_id,
                    date),
                drill_down_adjustment AS (
                    SELECT
                        id, 
                        author_id,
                        instrument_code_id,
                        date,
                        price,
                        quantity,
                        invested,
                        cum_quantity,
                        cum_invested,
                        IIF(
                    adjustment = 0 
                    AND LAG(adjustment) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date) <> 0,
                    LAG(adjustment) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date),
                    adjustment
                ) AS adjustment,
                        operation
                    FROM
                        investments
                ),
                investments_adj AS(
                    SELECT
                        id, 
                        author_id,
                        instrument_code_id,
                        date,
                        price,
                        quantity,
                        invested,
                        cum_quantity,
                        cum_invested  
                        + COALESCE(LAG(adjustment) OVER (PARTITION BY author_id, instrument_code_id ORDER BY date),0)
                        AS cum_invested,
                        adjustment,
                        operation
                    FROM
                        drill_down_adjustment
                ),
                investments_recalculation AS (
                    SELECT
                        id, 
                        author_id,
                        instrument_code_id,
                        date,
                        price,
                        quantity,
                        invested,
                        cum_quantity,
                        cum_invested ,
                        operation,
                        IIF(operation = 'Buy',ROUND((price * cum_quantity) - cum_invested,2),0)  as urgl,
                        IIF(operation = 'Sell',ROUND((price * cum_quantity) - cum_invested,2),0) as rgl
                    FROM investments_adj
                )

            SELECT 
					Investment.*,
					Instrument.instrument_code AS instrument_code,
					Instrument.instrument_name AS instrument_name
			   FROM investments_recalculation Investment
			   JOIN finance_instrument instrument
			   ON 1 = 1
				AND Investment.instrument_code_id = instrument_code_id""" % (request.user.id)

    with connections['default'].cursor() as cursor:
        cursor.execute(investment_evolution_query)
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()

    investment_evolution = []
    for row in rows:
        investment_evolution.append(dict(zip(columns, row)))

    with connections['default'].cursor() as cursor:
        cursor.execute(investment_summary_query)
        columns = [col[0] for col in cursor.description]  # Get column names
        rows = cursor.fetchall()

    investment_summary = []
    for row in rows:
        investment_summary.append(dict(zip(columns, row)))

    total_rgl = round(sum(item['RGL'] for item in investment_summary if item['RGL'] is not None),2)
    total_urgl = round(sum(item['URGL'] for item in investment_summary if item['URGL'] is not None),2)

    contex = {
        'investments_list': investments_list,
        'investments_count': investments_count,
        'investment_evolution': investment_evolution,
        'investment_summary': investment_summary,
        'total_rgl': total_rgl,
        'total_urgl': total_urgl
    }

    return render(request, 'finance/investment.html',contex)