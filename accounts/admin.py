from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm , UserChangeForm
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        ('User Information',{'fields':('username' , 'name' , 'lastname' , 'email' , 'password'),}),
        ('Permission',{'fields':('is_active','is_admin','is_superuser'),}),
    )

    add_fieldsets = (
        ('Creating Account',{'fields':('username' , 'name' , 'lastname' , 'email','password','password2'),}),
    )

    list_display = ['id','username','name','lastname', 'email' ,'is_active','is_admin','is_superuser']
    list_filter = ['is_active','is_admin','is_superuser']
    search_fields = ['username']
    ordering = ['-id']
    filter_horizontal = ()


admin.site.register(User,UserAdmin)