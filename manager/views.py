from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from manager.models import Worker, Task


@login_required
def index(request):
    """View function for the home page of the site."""
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    task_is_done_true = Task.objects.filter(is_completed=True).count()
    task_is_done_false = Task.objects.filter(is_completed=False).count()

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "task_is_done_true": task_is_done_true,
        "task_is_done_false": task_is_done_false
    }

    return render(request, "manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    template_name = "manager/worker_list.html"


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks__task_type")
    template_name = "manager/worker_detail.html"






