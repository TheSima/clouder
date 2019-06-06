from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
def validate_user_unique_email_login(email_login):
    try:
        user_by_username = User.objects.get(username=email_login)
        user_by_email = User.objects.get(email=email_login)
        if user_by_username is not None or user_by_email is not None:
            raise ValidationError(
                _('%(email_login)s already used'),
                params={'email_login': email_login},
            )
    except User.DoesNotExist:
        pass
