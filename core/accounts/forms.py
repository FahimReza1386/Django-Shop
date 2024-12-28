from django.contrib.auth import forms as auth_forms
from .models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class AuthenticationsForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationsForm, self).confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError(_("your user not verified ."))    