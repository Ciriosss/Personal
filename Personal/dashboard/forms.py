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