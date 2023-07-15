from django.urls import path

from manager.views import (
    index,
    register_user,
    WorkerListView,
    WorkerDetailView,
    TaskListView,
    TaskDetailView,

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
    )
]

app_name = "manager"
