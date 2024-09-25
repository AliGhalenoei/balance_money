from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import  render , redirect
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .forms import UserLoginForm , UserRegisterForm
from .models import User

# User Login View
class UserLoginView(View):

    form_class = UserLoginForm
    template_name = 'accounts/login_page.html'

    def get(self , request):
        return render(request,self.template_name , {'form':self.form_class})
    
    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username = cd['username'] , password = cd['password'])
            if user is not None:
                login(request,user)
                return redirect('home')
        return render(request,self.template_name,{'form':form})
    
# User Register View
class UserRegisterView(View):

    form_class = UserRegisterForm
    template_name = 'accounts/register_page.html'

    def get(self , request):
        return render(request,self.template_name,{'form':self.form_class})
    
    def post(self , request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            create_account = User.objects.create_user(
                username = cd['username'],
                name = cd['name'],
                lastname = cd['lastname'],
                email = cd['email'],
                password = cd['password']
            )
            login(request,create_account,backend="django.contrib.auth.backends.ModelBackend")
            return redirect('home')
        return render(request,self.template_name,{'form':form})
    
# User Logout View
class UserLogoutView(View):
    def get(self , request):
        logout(request)
        return redirect('login') 

# Reset Password Users  
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/reset_password/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'accounts/reset_password/password_reset_email.html'

class UserPasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'accounts/reset_password/password_reset_done.html'

class UserPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/reset_password/password_reset_confirm.html'
    success_url = reverse_lazy('login')