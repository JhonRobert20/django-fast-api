import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Description: Customized User Model"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("User name"),
        help_text="This is your name. You can leave it "
        "blank if you don't want to share it.",
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        help_text="This is your last name. You can leave it blank "
        "if you don't want to share it.",
        max_length=150,
        null=True,
        blank=True,
    )
    company_name = models.CharField(
        verbose_name=_("Company name"),
        help_text="This is the name of the company you work for. "
        "You can leave it blank if you don't work for a company.",
        max_length=150,
        null=True,
        blank=True,
    )

    password = models.CharField(_("password"), max_length=100)  # type: str
    email = models.EmailField(
        verbose_name=_("Email address"),
        blank=True,
        null=True,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        # Return the first part of the email address if not exists name
        return self.name or self.email.split("@")[0] if self.email else str(self.id)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
