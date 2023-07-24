from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.super_user = get_user_model().objects.create_superuser(
            username="test_super_user",
            password="super1qazcde3"
        )
        self.client.force_login(self.super_user)
        self.position = Position.objects.create(name="Test Position")
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="worker1qazcde3",
            position=self.position,
        )

    def test_worker_position_listed(self) -> None:
        url = reverse("admin:manager_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_worker_detailed_position_listed(self) -> None:
        url = reverse("admin:manager_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)
