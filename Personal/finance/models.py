from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class AssetClass(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Instrument(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=255)
    type = models.ForeignKey(AssetClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.instrument
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=255)
    type = models.ForeignKey(AssetClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.account
    
class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now) 
    instrument = models.ForeignKey(Instrument,on_delete = models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Investment({self.id})"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    def __str__(self):
        return self.category
    
class Label(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    def __str__(self):
        return self.label
       
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    label = models.ForeignKey(Label,on_delete = models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction({self.id})"

class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.author.id}-{self.date.strftime('%Y-%m')}-{self.account}"


