from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class NoSpacePasswordValidator:
    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(
                _("Your password can't contain spaces."),
                code='password_contains_space',
            )

    def get_help_text(self):
        return _("Your password can't contain spaces.")
