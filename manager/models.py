from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(
        max_length=60,
        unique=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["username"]

    def __str__(self) -> str:
        return (
            f"{self.username} ({self.first_name} {self.last_name} , "
            f"position: {self.position.name})"
        )


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
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["deadline", "name"]

    def __str__(self) -> str:
        return f"Task: {self.name}, priority of task : {self.priority}"
