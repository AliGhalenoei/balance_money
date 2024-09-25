from typing import Any
from django.db import models
from django_jalali.db import models as jmodels
from jalali_date import date2jalali , datetime2jalali

from accounts.models import User


class SavingMoney(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE,related_name='saving')
    money = models.DecimalField(max_digits=12,decimal_places=0 ,default=0)

    def __str__(self) -> str:
        return str(self.money)
    
class Category(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Transaction(models.Model):

    Transaction_Type = (
        ('income','درآمد'),
        ('cost','هزینه'),
    )

    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='user_transactions')
    category = models.ForeignKey(Category , on_delete=models.CASCADE , related_name='category_transactions')
    title = models.CharField(max_length=255)
    transaction = models.DecimalField(max_digits=12,decimal_places=0 ,default=0)
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    caption = models.TextField(null=True,blank=True)
    transaction_type = models.CharField(max_length=6 , choices=Transaction_Type)

    def __str__(self) -> str:
        return self.title
    
    def get_jalali_date(self):
        return datetime2jalali(self.date)
    
