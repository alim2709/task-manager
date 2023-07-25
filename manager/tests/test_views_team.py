from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Team

TEAM_LIST_URL = reverse("manager:team-list")


class PublicTaskListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(TEAM_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/teams/")


class PrivateTaskListTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for team_id in range(8):
            Team.objects.create(
                name=f"Test Team {team_id}",
            )

    def setUp(self) -> None:
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="worker1qazcde3",
        )
        self.client.force_login(self.worker)

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get("/teams/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(TEAM_LIST_URL)

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(TEAM_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/team_list.html")

    def test_correct_pagination_on_first_page(self) -> None:
        response = self.client.get(TEAM_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["team_list"]), 5)

    def test_correct_pagination_on_second_page(self) -> None:
        response = self.client.get(TEAM_LIST_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["team_list"]), 3)
