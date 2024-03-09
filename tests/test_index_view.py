from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType


class PublicIndexTest(TestCase):
    def test_index_login_required(self) -> None:
        url = reverse("kitchen:index")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/"
        )


class PrivateIndexTest(TestCase):
    def setUp(self) -> None:
        num_cooks = 4
        num_dish_types = 2
        for cook_id in range(num_cooks):
            get_user_model().objects.create_user(
                username=f"test username {cook_id}",
                password=f"test12{cook_id}",
                years_of_cooking=cook_id
            )

        for dish_type_id in range(num_dish_types):
            DishType.objects.create(
                name=f"test dish type {dish_type_id}",
            )

        test_dish1 = Dish.objects.create(
            name="test dish 1",
            price=19,
            dish_type_id=1,
        )
        test_dish2 = Dish.objects.create(
            name="test dish 2",
            price=21,
            dish_type_id=2,
        )

        test_dish1.cooks.set(get_user_model().objects.all()[:2])
        test_dish2.cooks.set(get_user_model().objects.all()[2:])

        test_dish1.save()
        test_dish2.save()

        self.client.login(
            username="test username 0",
            password="test120",
        )

    def test_index_correct_template(self) -> None:
        response = self.client.get(reverse("kitchen:index"))

        self.assertEqual(str(response.context["user"]), "test username 0 ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "kitchen/index.html")

    def test_index_num_cooks(self) -> None:
        response = self.client.get(reverse("kitchen:index"))

        self.assertEqual(response.context["num_cooks"], 4)

    def test_index_num_dishes(self) -> None:
        response = self.client.get(reverse("kitchen:index"))

        self.assertEqual(response.context["num_dishes"], 2)

    def test_index_num_dish_types(self) -> None:
        response = self.client.get(reverse("kitchen:index"))

        self.assertEqual(response.context["num_dish_types"], 2)
