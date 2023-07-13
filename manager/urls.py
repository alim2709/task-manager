from django.urls import path

from manager.views import index, WorkerListView, WorkerDetailView

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
    )
]

app_name = "manager"
