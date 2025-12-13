
from django.db import models
from django.utils import timezone
from user.models import Profile

class AssetClass(models.Model):
    id = models.AutoField(primary_key=True)
    asset_class_name = models.CharField(max_length=255)

    def __str__(self):
        return self.asset_class_name

class Instrument(models.Model):
    id = models.AutoField(primary_key=True)
    instrument_code = models.CharField(max_length=10)
    instrument_name = models.CharField(max_length=255)
    account_class = models.ForeignKey(AssetClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.instrument_code
    
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=255)
    account_class = models.ForeignKey(AssetClass, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  

    def __str__(self):
        return self.account_name
    
class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now) 
    instrument_code = models.ForeignKey(Instrument,on_delete = models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_value(self):
        return float(round(self.price * self.quantity,2))

    def __str__(self):
        return f"{self.date}-{self.author}-{self.instrument_code}"

class TransactionCategory(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.category
    
class Label(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    def __str__(self):

        return self.label
    
transaction_types = [
    ('Income', 'Income'),
    ('Expense', 'Expense'),
    ('Transfer', 'Transfer')
]
       
class Transaction(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    type = models.TextField(choices=transaction_types, default='Income')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    label_id = models.ForeignKey(Label, on_delete=models.SET_NULL, blank=True, null=True) 
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    account_id_secondary = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='secondary_transactions', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction-{self.id}"

class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    account_id = models.ForeignKey(Account,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.author.id}-{self.date.date()}-{self.account_id}"
