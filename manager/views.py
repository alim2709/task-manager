from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from .forms import ContactForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from manager.forms import (
    SignUpForm,
    TaskProjectForm,
    WorkerSearchForm,
    TaskSearchForm,
    TaskTypeSearchForm,
    PositionSearchForm,
    PositionForm,
    ProjectForm,
    TeamForm,
    TeamSearchForm,
    ProjectSearchForm,
    TaskForm,
)
from manager.models import Worker, Task, Position, TaskType, Team, Project


@login_required
def index(request):
    """View function for the home page of the site."""
    num_projects = Project.objects.count()
    num_teams = Team.objects.count()
    task_is_done_true = Task.objects.filter(is_completed=True).count()

    context = {
        "num_projects": num_projects,
        "num_teams": num_teams,
        "task_is_done_true": task_is_done_true,
    }

    return render(request, "manager/index.html", context=context)


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            authenticate(username=username, password=raw_password)
            msg = "User created - please " f'<a href="{reverse("login")}">login</a>.'
            success = True
        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/register.html",
        {"form": form, "msg": msg, "success": success},
    )


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    template_name = "manager/worker_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks__task_type")
    template_name = "manager/worker_detail.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]
    template_name = "manager/worker_update.html"

    def get_success_url(self):
        worker_id = self.kwargs["pk"]
        return reverse_lazy("manager:worker-detail", kwargs={"pk": worker_id})


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "manager/task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = (
            Task.objects.all().select_related("task_type").order_by("is_completed")
        )
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all().select_related("task_type")
    template_name = "manager/task_detail.html"


class TaskCreateWithProjectView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskProjectForm
    success_url = reverse_lazy("manager:project-detail")
    template_name = "manager/task_project_form.html"

    def get(self, request, project_pk, *args, **kwargs):
        self.project_pk = project_pk
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, project_pk, *args, **kwargs):
        self.project_pk = project_pk
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_pk"] = self.project_pk
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["project_pk"] = self.project_pk
        return form_kwargs

    def get_success_url(self):
        return reverse("manager:project-detail", kwargs={"pk": self.project_pk})


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_form.html"


class TaskProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskProjectForm
    template_name = "manager/project_task_update.html"

    def get(self, request, project_pk, *args, **kwargs):
        self.project_pk = project_pk
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, project_pk, *args, **kwargs):
        self.project_pk = project_pk
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_pk"] = self.project_pk
        return context

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["project_pk"] = self.project_pk
        return form_kwargs

    def get_success_url(self):
        return reverse("manager:project-detail", kwargs={"pk": self.project_pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_form.html"


class CompletedTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.filter(is_completed=True)
    paginate_by = 5
    template_name = "manager/completed_task_list.html"


@login_required
def task_completed_true(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not task.is_completed:
        task.is_completed = True
        task.save()
    return HttpResponseRedirect(reverse_lazy("manager:task-detail", args=[pk]))


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    template_name = "manager/task_confirm_delete.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5
    template_name = "manager/position_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_form.html"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")
    template_name = "manager/position_confirm_delete.html"


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    context_object_name = "task_type_list"
    template_name = "manager/task_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    queryset = TaskType.objects.all()
    context_object_name = "task_type_detail"
    template_name = "manager/task_type_detail.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    context_object_name = "task_type_form"
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    fields = "__all__"
    context_object_name = "task_type_delete"
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_confirm_delete.html"


@login_required
def toggle_assign_to_task(request, pk):
    worker = get_object_or_404(Worker, id=request.user.id)
    task = get_object_or_404(Task, pk=pk)
    projects = worker.teams.values_list("projects", flat=True)
    if task.project:
        if task in worker.tasks.all():
            worker.tasks.remove(pk)
        elif task not in worker.tasks.all() and task.project in projects:
            worker.tasks.add(pk)
        else:
            messages.info(request, "You need to be a member of team who is in project")
    elif task in worker.tasks.all():
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)

    return HttpResponseRedirect(reverse_lazy("manager:task-detail", args=[pk]))


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5
    template_name = "manager/team_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TeamSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Team.objects.all()
        form = TeamSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.all().prefetch_related("members__teams__projects")
    template_name = "manager/team_detail.html"


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("manager:team-list")
    template_name = "manager/team_form.html"


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("manager:team-list")
    template_name = "manager/team_form.html"


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:team-list")
    template_name = "manager/team_confirm_delete.html"


@login_required
def toggle_assign_to_team(request, pk):
    worker = get_object_or_404(Worker, id=request.user.id)
    team = get_object_or_404(Team, pk=pk)
    if team in worker.teams.all():
        worker.teams.remove(pk)
    else:
        worker.teams.add(pk)
    return HttpResponseRedirect(reverse_lazy("manager:team-detail", args=[pk]))


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 3
    template_name = "manager/project_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    queryset = Project.objects.all().prefetch_related("team__projects__tasks")
    template_name = "manager/project-detail.html"

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["project_pk"] = pk
        return self.render_to_response(context)


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("manager:project-list")
    template_name = "manager/project_form.html"


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("manager:project-list")
    template_name = "manager/project_form.html"


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:project-list")
    template_name = "manager/project_confirm_delete.html"


@login_required
def project_completed_true(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.filter(is_completed=False).count()
    if not tasks:
        project.is_completed = True
        project.save()
    else:
        messages.error(
            request,
            (
                "It`s necessary to complete all tasks "
                "of project before finishing project"
            ),
        )
    return HttpResponseRedirect(reverse_lazy("manager:project-detail", args=[pk]))


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, "admin@example.com", ["admin@example.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Message sent.")
            return redirect("main:homepage")
    messages.error(
        request,
        (
            "It`s necessary to complete all tasks " "of project before finishing project"
        ),
    )

    form = ContactForm()
    return render(request, "manager/contact.html", {"form": form})
