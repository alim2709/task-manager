from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Position

POSITION_LIST_URL = reverse("manager:position-list")


class PublicPositionListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(POSITION_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/positions/")


class PrivatePositionListTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for uniq_position in "ABCDEFGH":
            Position.objects.create(
                name=f"Test Position {uniq_position}",
            )

    def setUp(self) -> None:
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="worker1qazcde3",
        )
        self.client.force_login(self.worker)

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get("/positions/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(POSITION_LIST_URL)

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(POSITION_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_list.html")

    def test_correct_pagination_on_first_page(self) -> None:
        response = self.client.get(POSITION_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["position_list"]), 5)

    def test_correct_pagination_on_second_page(self) -> None:
        response = self.client.get(POSITION_LIST_URL + "?page=2")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["position_list"]), 3)
