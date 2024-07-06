from django.contrib.auth.models import  BaseUserManager
from django.core.exceptions import ValidationError
from uuid import uuid4
class CustomeBaseUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone=None,user_id=None, password=None):
        
        if not email:
            raise ValidationError({'email': 'User must have an email address'})
        if not first_name:
            raise ValidationError({'first_name': 'User must have first name'})
        if not last_name:
            raise ValidationError({'last_name': 'User must have a last name'})  
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name=last_name,
            user_id= user_id if user_id else str(uuid4()),
            phone=phone
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,first_name, last_name, password=None):
        
        user = self.create_user(
            email=email,
            first_name= first_name,
            last_name=last_name,

        )

        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
        


