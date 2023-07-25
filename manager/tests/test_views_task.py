from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import TaskType, Task, Project

TASK_LIST_URL = reverse("manager:task-list")


class PublicTaskListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(TASK_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/tasks/")


class PrivateTaskListTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        task_type = TaskType.objects.create(name="Test Task Type")
        project = Project.objects.create(
            name="test project",
            description="test project details",
            deadline="2024-12-22",
        )
        for task_id in range(8):
            Task.objects.create(
                name=f"Test Task {task_id}",
                description="Test Description",
                deadline="2023-12-12",
                is_completed=False,
                priority="Low",
                task_type=task_type,
                project=project,
            )

    def setUp(self) -> None:
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="worker1qazcde3",
        )
        self.client.force_login(self.worker)

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get("/tasks/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(TASK_LIST_URL)

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(TASK_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_list.html")

    def test_correct_pagination_on_first_page(self) -> None:
        response = self.client.get(TASK_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["task_list"]), 5)

    def test_correct_pagination_on_second_page(self) -> None:
        response = self.client.get(TASK_LIST_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["task_list"]), 3)
