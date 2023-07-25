import datetime
import zoneinfo

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.forms import SignUpForm, TaskProjectForm, TaskForm, PositionForm
from manager.models import Position, Project, Team, Task, TaskType, Worker


class SignUpFormTest(TestCase):
    def test_sign_up_creation_form_is_valid(self) -> None:
        position = Position.objects.create(name="Test Position")
        form_data = {
            "username": "test_worker",
            "password1": "worker1qazcde3",
            "password2": "worker1qazcde3",
            "first_name": "Test First",
            "last_name": "Test Last",
            "position": position,
        }
        form = SignUpForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)


class TaskProjectFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        position = Position.objects.create(name="test position for workers")
        for worker_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_worker_{worker_id}",
                password="worker1qazcde3",
                position=position
            )

    def setUp(self) -> None:
        position = Position.objects.create(name="TestPosition")
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            position=position,
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_task_with_project_and_team_is_valid(self):
        project = Project.objects.create(
            name="Test project name",
            description="test description",
            deadline="2023-09-24",
            is_completed=False,
        )

        team = Team.objects.create(name="test team name")

        team.members.set(get_user_model().objects.all()[:5])
        project.team.add(team)
        task_type = TaskType.objects.create(name="test task type")
        assignees = Worker.objects.filter(teams__projects=project.pk)
        form_data = {
            "name": "testtask",
            "description": "test description",
            "project": project,
            "deadline": datetime.datetime(year=2023, month=9, day=24, tzinfo=zoneinfo.ZoneInfo(key='Europe/Kiev')),
            "priority": "Medium",
            "task_type": task_type,
            "assignees": assignees,
        }
        form = TaskProjectForm(data=form_data, project_pk=project.pk)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["name"], form_data["name"])
        self.assertEquals(form.cleaned_data["description"], form_data["description"])
        self.assertEquals(form.cleaned_data["project"], form_data["project"])
        self.assertEquals(form.cleaned_data["deadline"], form_data["deadline"])
        self.assertEquals(form.cleaned_data["priority"], form_data["priority"])
        self.assertEquals(form.cleaned_data["task_type"], form_data["task_type"])
        self.assertQuerysetEqual(form.cleaned_data["assignees"], form_data["assignees"])

    def test_update_task_with_project_and_team_with_non_valid_data(self):
        project = Project.objects.create(
            name="Test project name",
            description="test description",
            deadline="2023-12-24",
            is_completed=False,
        )
        team = Team.objects.create(name="test team name")
        team.members.set(get_user_model().objects.all()[:5])
        project.team.add(team)
        task_type = TaskType.objects.create(name="test task type")
        task = Task.objects.create(
            name="testtask",
            description="test description",
            project=project,
            deadline=datetime.datetime(year=2023, month=9, day=24, tzinfo=zoneinfo.ZoneInfo(key='Europe/Kiev')),
            priority="Medium",
            task_type=task_type,
        )

        new_deadline = datetime.datetime(year=2025, month=9, day=24, tzinfo=zoneinfo.ZoneInfo(key='Europe/Kiev'))

        response = self.client.post(
            reverse("manager:task-update-project", kwargs={"pk": task.id, "project_pk": project.pk}),
            data={
                "deadline": new_deadline,
                "project": project.pk
            }
        )
        self.assertEqual(response.status_code, 200)


class TaskFormTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        position = Position.objects.create(name="test position for workers")
        for worker_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_worker_{worker_id}",
                password="worker1qazcde3",
                position=position
            )

    def setUp(self) -> None:
        position = Position.objects.create(name="TestPosition")
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            position=position,
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_task_creation_without_project_and_team(self):
        task_type = TaskType.objects.create(name="test task type")
        assignees = get_user_model().objects.all()
        form_data = {
            "name": "testtask",
            "description": "test_description",
            "deadline": datetime.datetime(year=2023, month=9, day=24, tzinfo=zoneinfo.ZoneInfo(key='Europe/Kiev')),
            "priority": "Medium",
            "task_type": task_type,
            "assignees": assignees,
        }
        form = TaskForm(data=form_data)
        print(form.errors)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data["name"], form_data["name"])
        self.assertEquals(form.cleaned_data["description"], form_data["description"])
        self.assertEquals(form.cleaned_data["deadline"], form_data["deadline"])
        self.assertEquals(form.cleaned_data["priority"], form_data["priority"])
        self.assertEquals(form.cleaned_data["task_type"], form_data["task_type"])
        self.assertQuerysetEqual(form.cleaned_data["assignees"], form_data["assignees"])

    def test_update_task_with_non_valid_data(self):
        task_type = TaskType.objects.create(name="test task type")
        task = Task.objects.create(
            name="testtask",
            description="test description",
            deadline=datetime.datetime(year=2024, month=9, day=24, tzinfo=zoneinfo.ZoneInfo(key='Europe/Kiev')),
            priority="Medium",
            task_type=task_type,
        )

        new_deadline = datetime.datetime(year=2022, month=9, day=24, tzinfo=zoneinfo.ZoneInfo(key='Europe/Kiev'))

        response = self.client.post(
            reverse("manager:task-update", kwargs={"pk": task.id}),
            data={
                "deadline": new_deadline,
            }
        )
        self.assertEqual(response.status_code, 200)


class PositionFormTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="TestPosition")
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            position=position,
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_position_is_valid(self):
        form_data = {
            "name": "test position"
        }
        form = PositionForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_create_position_with_non_valid_data(self):
        form_data = {
            "name": "test position``1!@$$%$`"
        }
        form = PositionForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertNotEquals(form.cleaned_data, form_data)

