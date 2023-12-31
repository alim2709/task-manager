from django.urls import path

from manager.views import (
    index,
    register_user,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskCreateWithProjectView,
    TaskProjectUpdateView,
    TaskDeleteView,
    CompletedTaskListView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TaskTypeListView,
    TaskTypeDetailView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    project_completed_true,
    task_completed_true,
    toggle_assign_to_task,
    toggle_assign_to_team,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register_user, name="register"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/task-complete/", task_completed_true, name="task-complete"),
    path(
        "tasks/create/<int:project_pk>/",
        TaskCreateWithProjectView.as_view(),
        name="task-project-create",
    ),
    path(
        "tasks/<int:pk>/update/<int:project_pk>",
        TaskProjectUpdateView.as_view(),
        name="task-update-project",
    ),
    path("tasks/create-task/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/create-task/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "tasks/completed_tasks/",
        CompletedTaskListView.as_view(),
        name="completed-tasks",
    ),
    path(
        "tasks/<int:pk>/toggle-assign/",
        toggle_assign_to_task,
        name="toggle-task-assign",
    ),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete",
    ),
    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task_types/<int:pk>/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("task_types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path(
        "teams/<int:pk>/toggle-assign/",
        toggle_assign_to_team,
        name="toggle-team-assign",
    ),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path(
        "projects/<int:pk>/project-complete/",
        project_completed_true,
        name="project_completed",
    ),
]

app_name = "manager"
