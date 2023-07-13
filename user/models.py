from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import password_validation
from django.utils import timezone
# Create your models here.

#Role of user model
class Role(models.Model):
    role_choices =(('ad','ADMIN'),('ma','MANAGER'),('em', 'EMPLOYEE'))
    name = models.CharField(max_length=255, unique=True,blank=False, null=False)
    description = models.CharField(max_length=255,unique=True,blank=False, null=False)
    role = models.CharField(max_length=20,choices=role_choices,unique=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField()

    class Meta:
        db_table = 'role'

class MyUserManager(BaseUserManager):
    def create_user(self,full_name, email, phone_number, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            full_name = full_name,
            email=self.normalize_email(email),
            phone_number= phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            full_name,
            email,
            phone_number,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user       
    
class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=40, blank=False, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[EmailValidator,MinLengthValidator(16)], blank=False, null=False

    )
    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(10)], unique=True, blank=False, null=False)
    password = models.CharField(validators=[MinLengthValidator(8)], max_length=255,blank=False, null=False)
    url_img = models.TextField()
    address = models.TextField(blank=False,null=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    create_not_signup = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','phone_number']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, related_name='admin', on_delete=models.CASCADE) 
    role = models.ManyToManyField(Role)

    class Meta:
        db_table = 'admin'

class MasterChef(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    img_url = models.URLField(blank=False, null=True)
    year_exp = models.IntegerField(default=3)
    fb = models.TextField()
    twitter = models.TextField()
    youtube = models.TextField()
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master_chef'

class Opening(models.Model):
    weekday_start = models.CharField(max_length=15, blank=False, null=False, unique=True)
    weekday_end = models.CharField(max_length=15, default=None)
    time_open = models.TimeField(default=None)
    time_closed = models.TimeField(default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'opening'

class Restaurant(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    title = models.CharField(max_length=255, default=None)
    title_text = models.TextField(default=None)
    about_text = models.TextField(default=None)
    year_exp = models.IntegerField(default=3)
    url_img = models.TextField(default=None)
    
    class Meta:
        db_table = 'restaurant'
    
from django.contrib import admin
admin.site.register([Role,CustomUser,Admin,MasterChef,Opening,Restaurant])
