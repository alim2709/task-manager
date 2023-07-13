from django.urls import path

from manager.views import (
    index,
    WorkerListView,
    WorkerDetailView,
    TaskListView,
)

urlpatterns = [
    path("", index, name="index"),
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
    )
]

app_name = "manager"
