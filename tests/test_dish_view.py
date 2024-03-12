from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import DishType, Dish


URL_DISH_LIST = "kitchen:dish-list"


class PublicDishViewTest(TestCase):
    def test_dish_login_required(self) -> None:
        response = self.client.get(reverse(URL_DISH_LIST))

        self.assertRedirects(
            response,
            "/accounts/login/?next=/dishes/"
        )


class PrivateDishViewTest(TestCase):
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
                name=f"test dish_type {dish_type_id}",
            )

        test_dish1 = Dish.objects.create(
            name="test dish 1",
            price=20,
            dish_type_id=1,
        )
        test_dish2 = Dish.objects.create(
            name="test dish 2",
            price=21,
            dish_type_id=2,
        )

        test_dish1.cooks.set(get_user_model().objects.all()[:2])
        test_dish1.cooks.set(get_user_model().objects.all()[2:])

        test_dish1.save()
        test_dish2.save()

        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            years_of_cooking=6
        )

        self.client.force_login(self.user)

    def test_dish_correct_template(self) -> None:
        response = self.client.get(reverse(URL_DISH_LIST))

        self.assertEqual(str(response.context["user"]), "test_username ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_retrieve_dish_list(self) -> None:
        response = self.client.get(reverse(URL_DISH_LIST))
        dishes = Dish.objects.all()

        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes)
        )

    def test_dish_list_search(self) -> None:
        response = self.client.get(reverse(URL_DISH_LIST) + "?name=1")
        dish = Dish.objects.filter(name="test dish 1")

        self.assertEqual(
            list(response.context["dish_list"]),
            list(dish)
        )
