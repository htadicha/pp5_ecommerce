from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyAccountManager(BaseUserManager):
    """Custom user manager for Account model."""
    
    def create_user(self, first_name, last_name, username, email, password=None):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        """Create and save a superuser with the given email and password."""
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """Custom user model extending AbstractBaseUser."""
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        """Return the user's full name."""
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """Return the user's email as string representation."""
        return self.email

    def has_perm(self, perm, obj=None):
        """Check if user has specific permission."""
        return self.is_admin

    def has_module_perms(self, add_label):
        """Check if user has module permissions."""
        return True


class UserProfile(models.Model):
    """Extended user profile with additional information."""
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        """Return the user's first name as string representation."""
        return self.user.first_name

    def full_address(self):
        """Return the user's complete address."""
        return f'{self.address_line_1} {self.address_line_2}'


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile automatically when a new Account is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when Account is saved."""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

