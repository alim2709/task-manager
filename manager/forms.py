from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import NumberInput
from django.forms.utils import ErrorList
from django.utils import timezone

from manager.models import Worker, Task, Position, Project, Team


class SignUpForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class ProjectForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        label="Deadline", required=True, widget=NumberInput(attrs={"type": "date"})
    )
    team = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = ["name", "description", "deadline", "team"]


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskProjectForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        label="Deadline", required=True, widget=NumberInput(attrs={"type": "date"})
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "project",
            "deadline",
            "priority",
            "task_type",
            "assignees",
        ]
        widgets = {"project": forms.HiddenInput()}

    def __init__(
        self,
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        instance=None,
        use_required_attribute=None,
        renderer=None,
        project_pk=None,
    ):
        super().__init__(
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            instance,
            use_required_attribute,
            renderer,
        )
        self.initial["project"] = project_pk
        if project_pk:
            assignees = Worker.objects.filter(teams__projects=project_pk)
            self.fields["assignees"].queryset = assignees

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        now = timezone.now()
        project = self.cleaned_data["project"]
        if deadline < now:
            raise ValidationError("Deadline can't be earlier than current date")

        elif deadline.date() > project.deadline:
            raise ValidationError("Deadline can't be after deadline project")
        return deadline


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        label="Deadline", required=True, widget=NumberInput(attrs={"type": "date"})
    )

    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
        ]

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        now = timezone.now()

        if deadline < now:
            raise ValidationError("Deadline can't be earlier than current date")

        return deadline


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
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
        raise ValidationError("The position name should have at least two letters.")
    return position_name


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
