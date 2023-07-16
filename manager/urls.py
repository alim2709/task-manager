from django.urls import path

from manager.views import (
    index,
    register_user,
    WorkerListView,
    WorkerDetailView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    PositionListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", register_user, name="register"),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    )
]

app_name = "manager"
