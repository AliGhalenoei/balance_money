from typing import Any
from django.http import HttpRequest
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages

from transactions.forms import TransactionForm,EditTransactionForm , CategoryForm
from transactions.modules import filter_transaction , get_from_object , adjust_money , delete_or_trans
from transactions.models import Transaction , Category 
# Create your views here.


class HomePageView(View):

    template_name = 'content/index.html'

    def get(self,request):
        transactions = Transaction.objects.filter(date__month=timezone.now().month,user=request.user)
        income = transactions.filter(transaction_type='income').aggregate(Sum('transaction'))['transaction__sum'] or 0
        cost = transactions.filter(transaction_type='cost').aggregate(Sum('transaction'))['transaction__sum'] or 0

        context = {
        'income': income,
        'cost': cost,
        }
        return render(request, self.template_name , context=context)

class TransactionsPageView(View):
    
    edit_form_class = EditTransactionForm
    form_class = TransactionForm
    template_name = 'content/transactions_page.html'

    def get(self , request):
        incomes = filter_transaction('income')
        costs = filter_transaction('cost')
        
        return render(request,self.template_name,{
            'edit_transaction_form':self.edit_form_class,
            'form':self.form_class,
            'incomes':incomes,
            'costs':costs,
        })
    
    def post(self , request):
        user = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = user
            transaction.save()
            return redirect('home')
        return render(request,self.template_name,{'form':form})
    
class EditTransactionView(View):

    form_class = EditTransactionForm
    template_name = 'content/transactions_page.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.transaction_ins = get_from_object(Transaction,kwargs['transaction_id'])
        return super().setup(request, *args, **kwargs)
    
    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST,instance = self.transaction_ins)
        
        if form.is_valid():
            user = request.user
            transaction = form.save(commit=False)
            transaction.user = user
            transaction.save()
            adjust_money(user , transaction)
            return redirect('transactions')
        return redirect('transactions')

class DeleteTransactionView(View):
    
    def get(self , request , transaction_id):
        user = request.user
        transaction = get_object_or_404(Transaction,id=transaction_id)
        delete_or_trans(user,transaction)
        transaction.delete()
        return redirect('home')

class CategorysPageView(View):

    form_class = CategoryForm
    template_name = 'content/categorys_page.html'

    def get(self , request):
        categorys = Category.objects.filter(user_id=0)
        user_categorys = Category.objects.filter(user_id=request.user.id)
        return render(request,self.template_name,{
            'categorys':categorys,
            'user_categorys':user_categorys
        })
    
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user_id = request.user.id
            category.save()
            messages.success(request,'دسته شما با موفقیت اضافه شد')
            return redirect('categorys')
        return render(request,self.template_name,{'form':form})
    
class EditCategoryView(View):

    form_class = CategoryForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.category_instance = get_from_object(Category,kwargs['category_id'])
        return super().setup(request, *args, **kwargs)

    def post(self , request , *args , **kwargs):
        form = self.form_class(request.POST,instance=self.category_instance)
        
        if form.is_valid():
            category=form.save(commit=False)
            category.user_id = request.user.id
            category.save()
            messages.success(request,'تغیرات با موفقیت اعمال شد')
            return redirect('categorys')
        else:
            messages.success(request,'اختلال در انجام عملیات','danger')
            return redirect('categorys')
        
class DeleteCategoryView(View):

    def get(self , request , *args , **kwargs):
        category = get_from_object(Category,kwargs['category_id'])
        category.delete()
        messages.success(request,'دسته با موفقیت حذف شد')
        return redirect('categorys')

class NotFoundPageView(View):

    template_name = 'content/404.html'

    def get(self , request):
        return render(request,self.template_name)
