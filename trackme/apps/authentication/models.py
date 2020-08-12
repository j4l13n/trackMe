from django.db import models
from django.db.models import F
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)

from trackme.manager import BaseManager
from trackme.models import BaseModel
from trackme.utils.app_utils.generetors import \
    ID_LENGTH, id_generater


class UserManager(BaseUserManager, BaseManager):
    """
    User Manager class
    """

    def create_user(self, **kwargs):
        """
        Create a user method
        """
        username = kwargs.get("username")
        email = kwargs.get("email")
        phone_number = kwargs.get("phone_number")
        password = kwargs.get("password")

        check_email = self.model.objects.filter(email=email).first()
        check_username = \
            self.model.objects.filter(username=username).first()
        check_phone_number = self.model.objects.filter(
            phone_number=phone_number,
        ).first()
        if check_email:
            raise ValueError(
                "User with email {} already exists".format(email)
            )
        
        if username and check_username:
            raise ValueError(
                "User with username {} already exists".format(username)
            )

        if phone_number and check_phone_number:
            raise ValueError(
                "User with phone number {} already exists".format(phone_number)
            )
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Create super user method to your default database
        """
        user = self.create_user(email=email, password=password)
        user.is_superuser = user.is_staff = True
        user.is_active = user.is_admin = True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model
    """
    ALLOWED = 'AL'
    DISALLOWED = 'DIS'
    AGREEMENT_CHOICES = [
        (ALLOWED, 'Allowed'),
        (DISALLOWED, 'Disallowed'),
    ]
    id = models.CharField(
        max_length=ID_LENGTH,
        primary_key=True,
        default=id_generater,
        editable=False,
    )
    username =  models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    phone_number = models.CharField(max_length=100, null=True, unique=True)
    password = models.CharField(max_length=100)
    image = models.CharField(
        max_length=150, null=True, blank=True,
        default="https://res.cloudinary.com/julien/image/upload/"
        "v1594986765/user-avatar_nch70m.png")
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    agreement = models.CharField(
        max_length=3, 
        choices=AGREEMENT_CHOICES,
        default=DISALLOWED)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()
    all_objects = UserManager(alive_only=False)

    USERNAME_FIELD = "email"

    class Meta:
        """
        User's Meta data
        """
        verbose_name_plural = "Users"
        ordering = [F('username').asc(nulls_last=True)]

    def __str__(self):
        return self.username

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()
