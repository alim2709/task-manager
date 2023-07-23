from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from manager.models import Position


class PositionModelTest(TestCase):
    def setUp(self) -> None:
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="worker1qazcde3",
        )
        self.client.force_login(self.worker)

    def test_position_str(self) -> None:
        position = Position.objects.create(
            name="Test Position",
        )

        self.assertEquals(
            str(position),
            f"{position.name}"
        )

    def test_update_position_with_valid_data(self) -> None:
        position = Position.objects.create(
            name="Test Position",
        )
        new_name = "Test Position Updated"
        response = self.client.post(
            reverse("manager:position-update", kwargs={"pk": position.id}),
            data={"name": new_name},
        )

        self.assertEquals(response.status_code, 302)

    def test_update_position_with_not_valid_data(self) -> None:
        position = Position.objects.create(
            name="Test Position",
        )
        new_name = "Test Position !@#$%^"
        response = self.client.post(
            reverse("manager:position-update", kwargs={"pk": position.id}),
            data={"name": new_name},
        )
        self.assertEquals(response.status_code, 200)

    def test_delete_position(self) -> None:
        position = Position.objects.create(
            name="Test Position",
        )
        response = self.client.post(
            reverse("manager:position-delete", kwargs={"pk": position.id})
        )

        self.assertEquals(response.status_code, 302)
        self.assertFalse(
            Position.objects.filter(id=position.id).exists()
        )


class WorkerModelTest(TestCase):
    def setUp(self) -> None:
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="worker1qazcde3",
            first_name="Test First",
            last_name="Test Last",
        )
        self.client.force_login(self.worker)

    def test_worker_str(self) -> None:
        self.assertEquals(
            str(self.worker),
            f"{self.worker.username} ({self.worker.first_name} "
            f"{self.worker.last_name})"
        )

    def test_create_worker_with_position(self) -> None:
        username = "test_worker_create"
        password = "worker1qazcde3"
        position = Position.objects.create(
            name="Test Position",
        )

        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position,
        )

        self.assertEquals(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEquals(worker.position, position)

    def test_worker_get_absolute_url(self) -> None:
        self.assertEquals(
            self.worker.get_absolute_url(),
            "/workers/1/"
        )
