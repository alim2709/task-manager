from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from manager.models import Worker, Task


@login_required
def index(request):
    """View function for the home page of the site."""
    num_tasks = Task.objects.count()
    task_is_done_true = Task.objects.filter(is_completed=True).count()
    task_is_done_false = Task.objects.filter(is_completed=False).count()

    context = {
        "num_tasks": num_tasks,
        "task_is_done_true": task_is_done_true,
        "task_is_done_false": task_is_done_false
    }

    return render(request, "manager/index.html", context=context)





