from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(
        max_length=60,
        unique=True,
        default="worker"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["username"]

    def get_absolute_url(self):
        return reverse("manager:worker-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return (
            f"{self.username} ({self.first_name} {self.last_name})"
        )


class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Worker, related_name="teams")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=600)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField()
    team = models.ManyToManyField(Team, related_name="projects")

    class Meta:
        ordering = ["is_completed", "deadline", "name"]


    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low")
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")


    class Meta:
        ordering = ["deadline", "name", "is_completed"]

    def get_absolute_url(self):
        return reverse("manager:task-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"Task: {self.name}, priority of task : {self.priority}"





