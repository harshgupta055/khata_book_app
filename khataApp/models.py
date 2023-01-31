from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone:
            raise ValueError('The given username must be set')
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(blank=True, null=True)
    phone = models.BigIntegerField(unique=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)


class Worker(models.Model):
    STATUS_CHOICES = [
        ("WORKING", "WORKING"),
        ("PAUSE", "PAUSE"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    salary = models.FloatField(default=0.0, null=True)
    doj = models.DateField(blank=True, null=True)
    working_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='WORKING')

    def __str__(self) -> str:
        return self.name


class DailyWage(models.Model):
    TYPE_CHOICES = [
        ("SPEND", "SPEND"),
        ("GIVEN", "GIVEN"),
    ]
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="daily_wage")
    amount = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="SPEND")
    reason = models.CharField(max_length=255, default='-', null=True, blank=True)

    def __str__(self) -> str:
        return self.worker.name


class MonthWageGiven(models.Model):
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="monthly_wage")
    amount = models.FloatField(blank=True, default=0.0)
    pre_amount = models.FloatField(blank=True, default=0.0)
    month = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return self.worker.name


class TestTable(models.Model):
    name = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return self.name