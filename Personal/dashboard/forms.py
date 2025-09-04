from django import forms
from finance.models import *
from django.forms import formset_factory

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
        fields = ['date', 'type','amount','category_id','label_id','account_id','account_id_secondary','description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'label_id': forms.Select(attrs={'class': 'form-control'}),
            'account_id': forms.Select(attrs={'class': 'form-control'}),
            'account_id_secondary': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'type': 'Type',
            'amount': 'Amount',
            'category_id':'Category',
            'label_id':'Label',
            'account_id':'Payment Account',
            'account_id_secondary':'Receiving Account',
            'description':'Description'
        }

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['label']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'label': 'Label'
        }

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['date', 'instrument_code', 'quantity', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'instrument_code': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'step': '0.0000000001', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }
        labels = {
            'date': 'Date',
            'instrument_code': 'Instrument',
            'quantity': 'Quantity',
            'price': 'Price'
        }



class WalletForm(forms.Form):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        initial=timezone.now,
        label="Date"
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label="Note"
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        accounts = Account.objects.filter(author=user)
        for account in accounts:
            field_name = f'account_{account.id}'
            self.fields[field_name] = forms.DecimalField(
                max_digits=10,
                decimal_places=2,
                required=False,
                initial=0,
                label=f"{account.account_name} Amount",
                widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
            )