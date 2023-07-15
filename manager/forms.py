from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.models import Worker


class SignUpForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )

