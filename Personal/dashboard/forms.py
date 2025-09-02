from django import forms
from finance.models import *

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_name', 'account_class']
        widgets = {
            'account_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter account name'
            }),
            'account_class': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'account_name': 'Account Name',
            'account_class': 'Account Class',
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'amount','category_id','label_id','account_id','description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'label_id': forms.Select(attrs={'class': 'form-control'}),
            'account_id': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'amount': 'Amount',
            'category_id':'Category',
            'label_id':'Label',
            'account_id':'Account',
            'description':'Description'
        }