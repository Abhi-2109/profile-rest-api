from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.

class UserProfileManager(BaseUserManager):
    """ Helps Django work with our custom user model"""

    def create_user(self,email,name,password=None):
        """ Creates a nw user profile object. """

        if not email:
            raise ValueError("Users must have an email address.")

        # normalize means to convert it into email format means lowercase
        email = self.normalize_email(email)
        user = self.model(email= email, name = name)

        # The set password Function will encrpt the password for us
        # This is best way to make a secure system
        # The hash code generated by this function will get save in the database
        user.set_password(password)
        user.save(using = self._db)

        return user

    # Function to create Super user
    # It has full control over the system
    def create_superuser(self,email,name,password):
        """ creates and saves a new superuser with give details"""
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using = self._db)



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represent a user profile inside our system
    """
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)

    # To see user is active or not
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    # It is used as a username to login
    # A standard django has USERNAME_FIELD. It is like a handle to login
    # replacing it with Email
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS Are the fields that are required for all the USER
    # We do not put EMAIL because It is USERNAME_FIELD. So it will be already required
    REQUIRED_FIELDS = ['name']

    # Helper Function

    def get_full_name(self):
        """
            Used to get a user full name.
        """
        return self.name

    def get_short_name(self):
        """Used to get a users short name """

        return self.name

    def __str__(self):
        """
        Django uses this when it needs to convert the Object to a string
        """
        return self.email
