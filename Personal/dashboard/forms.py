from django import forms
from django.utils import timezone
from finance.models import *
from fitness.models import *


####################################
#######     FINANCE FORMS    #######
####################################


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
    date = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Transaction
        fields = ['date', 'type','amount','category_id','label_id','account_id','account_id_secondary','description']
        widgets = {
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
    date = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Investment
        fields = ['date', 'instrument_code', 'quantity', 'price']
        widgets = {
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

####################################
#######     FITNESS FORMS    #######
####################################

class BodyForm(forms.ModelForm):
    date = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    class Meta:
        model = Body
        fields = ['date', 'weight', 'waist', 'bicept', 'leg', 'BMI', 'muscle_mass', 'fat_mass', 'body_water', 'visceral_fat', 'metabolic_age']
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter weight in kg'
            }),
            'waist': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter waist measurement in cm'
            }),
            'bicept': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter bicep measurement in cm'
            }),
            'leg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter leg measurement in cm'
            }),
            'BMI': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter BMI'
            }),
            'muscle_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter muscle mass in kg'
            }),
            'fat_mass': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter fat mass in kg'
            }),
            'body_water': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter body water percentage'
            }),
            'visceral_fat': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Enter visceral fat level'
            }),
            'metabolic_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter metabolic age in years'
            }),
        }
        labels = {
            'date': 'Measurement Date',
            'weight': 'Weight (kg)',
            'waist': 'Waist Circumference (cm)',
            'bicept': 'Bicep Circumference (cm)',
            'leg': 'Leg Circumference (cm)',
            'BMI': 'Body Mass Index',
            'muscle_mass': 'Muscle Mass (kg)',
            'fat_mass': 'Fat Mass (kg)',
            'body_water': 'Body Water (%)',
            'visceral_fat': 'Visceral Fat Level',
            'metabolic_age': 'Metabolic Age (years)',
        }

class PhysicalActivityForm(forms.ModelForm):
    date = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    class Meta:
        model = PhisicalActivity
        fields = ['date', 'time', 'type', 'intensity']
        widgets = {
            'time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter duration in minutes'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'intensity': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'date': 'Activity Date',
            'time': 'Duration (minutes)',
            'type': 'Exercise Type',
            'intensity': 'Intensity Level',
        }


class DietForm(forms.ModelForm):
    date = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    class Meta:
        model = Diet
        fields = ['date', 'need_cal', 'eaten_cal']
        widgets = {
            'need_cal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter required calories'
            }),
            'eaten_cal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Enter consumed calories'
            }),
        }
        labels = {
            'date': 'Diet Date',
            'need_cal': 'Required Calories',
            'eaten_cal': 'Consumed Calories',
        }