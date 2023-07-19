from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.forms import NumberInput
from django.utils import timezone

from manager.models import Worker, Task, Position, Project


class SignUpForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(label="Date", required=True, widget=NumberInput(attrs={'type': 'date'}))

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        now = timezone.now()

        if deadline < now:
            raise ValidationError(
                "Deadline can't be earlier than current date"
            )

        return deadline


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ("name",)

    def clean_name(self):
        return validate_position_name(self.cleaned_data["name"])


def validate_position_name(position_name):
    if not all(char.isalpha() or char.isspace() for char in position_name):
        raise ValidationError(
            "Characters in the position name can be only alphabetic or spaces."
        )
    if len(position_name) < 2:
        raise ValidationError(
            "The position name should have at least two letters."
        )
    return position_name


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
