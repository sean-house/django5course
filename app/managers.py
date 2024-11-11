from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a User with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user. Defaults to None.
            **extra_fields: Additional keyword arguments to be saved in the User model.

        Returns:
            User: The newly created User.

        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a superuser with the given email and password.

        Args:
            email (str): The email address of the superuser.
            password (str): The password of the superuser. Defaults to None.
            **extra_fields: Additional keyword arguments to be saved in the User model.

        Returns:
            User: The newly created superuser.

        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
