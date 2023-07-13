from django.urls import path

from manager.views import index, WorkerListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    path()
]

app_name = "manager"
