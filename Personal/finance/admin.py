from django.contrib import admin
from .models import *

admin.site.register([AssetClass, Instrument, Account, Investment, TransactionCategory, Label, Transaction])
