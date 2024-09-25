from django.urls import path 
from .import views

urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    # password reset urls
    path('password/reset/form/',views.UserPasswordResetView.as_view(),name='password_reset'),
    path('password/reset/done/',views.UserPasswordResetDone.as_view(),name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/',views.UserPasswordResetConfirm.as_view(),name='password_reset_confirm'),
]