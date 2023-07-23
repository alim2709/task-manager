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
