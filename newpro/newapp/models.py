from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import UserManager
from django.core.validators import RegexValidator
from django.db import models



class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')

        email=self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_staffuser(self, email, password=None):

        user = self.create_user(email, password=password,)
        user.is_staff=True
        return user


    def create_superuser(self, email, password):

        user = self.create_user(email,password=password,)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username', 'phone']

    objects=UserManager()

class User(AbstractBaseUser):

    email = models.EmailField(verbose_name='email address', max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=False, default='')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                 message="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=10, unique=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class PhoneOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex =r'^\+?1?\d{9,14}$',message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)