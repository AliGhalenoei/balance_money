from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self , username , name , lastname , email , password):
        if not username:
            raise ValueError('Error Username!!!')
        if not name:
            raise ValueError('Error Name!!!')
        if not lastname:
            raise ValueError('Error Lastname!!!')
        
        
        user = self.model(
            username = username,
            name=name,
            lastname=lastname,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self , username , name , lastname , email , password):
        user = self.create_user(username , name , lastname , email , password)
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user