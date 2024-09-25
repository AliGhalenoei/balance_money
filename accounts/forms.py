import re
from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model


User = get_user_model()
# Coustom User Form
class UserCreationForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'name' , 'username' , 'email' )

    def save(self, commit: bool = True) :
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise ValidationError('passwords is not match!!!')
        return cd['password2']
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('__all__')

# Form Login Users
class UserLoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')

    def __init__(self , *args , **kwargs):
        super(UserLoginForm,self).__init__(*args , **kwargs)
        # self.fields['username'].error_messages = {'required': 'custom required message'}

        # change all message required fields
        for field in self.fields.values():
            field.error_messages = {'required':'پر کردن این بخش اجباری است'}

    def clean_username(self):
        data_user = self.cleaned_data.get('username')
        
        if "@" in data_user:
            user = User.objects.filter(email=data_user).exists()
            if not user:
                raise ValidationError('اطلاعات نامعتبر است. لطفا از صحیح بودن آن اطمینان حاصل فرمایید')
        else:
            user = User.objects.filter(username=data_user).exists()
            if not user:
                raise ValidationError('اطلاعات نامعتبر است. لطفا از صحیح بودن آن اطمینان حاصل فرمایید')

        return data_user

# Form Register Users
class UserRegisterForm(forms.Form):
            
    username = forms.CharField(label='username')
    name = forms.CharField(label='name')
    lastname = forms.CharField(label='lastname')
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')
    password2 = forms.CharField(label='password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args , **kwargs)

        # change all message required fields
        for field in self.fields.values():
            field.error_messages = {'required':'پر کردن این بخش اجباری است'}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username = username).exists()

        # بررسی شرایط نام کاربری
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d_]+$', username):
            raise ValidationError('نام کاربری باید شامل حروف بزرگ، حروف کوچک و اعداد باشد و می‌تواند شامل _ نیز باشد')

        if user:
            raise ValidationError('کاربری قبلا با این نام ثبت نام کرده است')
        
        return username
    
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # بررسی اینکه آیا نام فقط شامل کاراکترهای فارسی است
        if not re.match(r'^[\u0600-\u06FF\s]+$', name):
            raise forms.ValidationError("نام باید فارسی باشد")
        
        return name
    
    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')

        # بررسی اینکه آیا نام فقط شامل کاراکترهای فارسی است
        if not re.match(r'^[\u0600-\u06FF\s]+$', lastname):
            raise forms.ValidationError("نام خانوادگی باید فارسی باشد")
        
        return lastname
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email = email).exists()

        if user:
            raise ValidationError('نشانی ایمیل از قبل وجود دارد')
        return email
    
    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        password2 = cd.get('password2')

        if len(password) < 8 :
            raise ValidationError('گذرواژه باید حداکثر ۸ رقم باشد')

        if password and password2 and password != password2:
            raise ValidationError('گذرواژه ها با هم مطابقت ندارد')
        



    
