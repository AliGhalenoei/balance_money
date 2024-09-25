from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from .models import Transaction , Category



class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ('user',)

    def __init__(self , *args , **kwargs):
        super(TransactionForm,self).__init__(*args , **kwargs)
        self.fields['date'] = JalaliDateField(widget=AdminJalaliDateWidget)


class EditTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ('user','date')

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)
