from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
# Register your models here.
from .models import *


admin.site.register(SavingMoney)
admin.site.register(Category)

@admin.register(Transaction)
class TransactionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title' , 'date']