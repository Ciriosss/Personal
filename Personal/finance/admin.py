from django.contrib import admin
from .models import *

admin.site.register([AssetClass,Instrument,Account,Investment,Category,Label,Transaction,Wallet])