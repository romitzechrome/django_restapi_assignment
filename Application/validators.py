from django.core.exceptions import ValidationError
from .models import User, Course


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            f"{value} is taken.",
            params={'value': value}
        )


def validate_course(value):
    if Course.objects.filter(Course=value).exists():
        raise ValidationError(
            f'{value} is already exist..',
            params={'value': value}
        )
