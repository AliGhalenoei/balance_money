from django.urls import path 
from .import views

urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('transactions/',views.TransactionsPageView.as_view(),name='transactions'),
    path('edit/transaction/<int:transaction_id>/',views.EditTransactionView.as_view(),name='edit_transaction'),
    path('delete/transaction/<int:transaction_id>/',views.DeleteTransactionView.as_view(),name='delete_transaction'),
    path('categorys/',views.CategorysPageView.as_view(),name='categorys'),
    path('edit/category/<int:category_id>/',views.EditCategoryView.as_view(),name='edit_category'),
    path('delete/category/<int:category_id>/',views.DeleteCategoryView.as_view(),name='delete_category'),
    path('404/',views.NotFoundPageView.as_view(),name='404'),
]