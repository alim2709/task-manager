from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Task, Position, TaskType, Project, Team


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("deadline", "name")
    list_filter = ("task_type",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("deadline", "name")
    list_filter = ("team",)


admin.site.register(Position)
admin.site.register(TaskType)
admin.site.register(Team)
