"""Custom user model and related domain logic."""
from __future__ import annotations

from decimal import Decimal

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    """Custom manager for the user model."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Application user model using e-mail as the primary identifier."""

    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        PRODUCER = "producer", _("Producer")
        ACCOUNT_MANAGER = "account_manager", _("Account Manager")

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)
    
    # Legacy role field - kept for backwards compatibility
    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.ACCOUNT_MANAGER,
        help_text="Primary role (informational). Use capability flags for actual permissions.",
    )
    
    # Capability flags - user can have multiple capabilities
    can_produce = models.BooleanField(
        default=False,
        help_text="User can be assigned as a producer on policies.",
    )
    can_manage_accounts = models.BooleanField(
        default=False,
        help_text="User can be assigned as an account manager on policies.",
    )
    
    # Default commission rates (can be overridden per-policy)
    default_producer_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Default producer commission rate (%). Can be overridden per policy.",
    )
    default_account_manager_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Default account manager commission rate (%). Can be overridden per policy.",
    )
    
    # Keep for backwards compatibility, maps to default_producer_rate
    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Deprecated. Use default_producer_rate or default_account_manager_rate.",
    )
    
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
