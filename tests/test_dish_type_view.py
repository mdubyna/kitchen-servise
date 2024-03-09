from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType


URL_DISH_TYPE_LIST = "kitchen:dish-type-list"


class PublicDishTypeViewTest(TestCase):
    def test_manufacturer_login_required(self) -> None:
        response = self.client.get(reverse(URL_DISH_TYPE_LIST))

        self.assertRedirects(
            response,
            "/accounts/login/?next=/dish-types/"
        )


class PrivateDishTypeViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )

        self.client.force_login(self.user)

    def test_dish_type_correct_template(self) -> None:
        response = self.client.get(reverse(URL_DISH_TYPE_LIST))

        self.assertEqual(str(response.context["user"]), "test_username ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_retrieve_dish_type_list(self) -> None:
        DishType.objects.create(
            name="Pizza",
        )
        DishType.objects.create(
            name="Sushi",
        )

        response = self.client.get(reverse(URL_DISH_TYPE_LIST))
        manufacturers = DishType.objects.all()

        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(manufacturers)
        )

    def test_dish_type_list_search(self) -> None:
        DishType.objects.create(
            name="Pizza",
        )
        DishType.objects.create(
            name="Sushi",
        )

        response = self.client.get(
            reverse(URL_DISH_TYPE_LIST) + "?name=Pizza"
        )
        pizza = DishType.objects.filter(name="Pizza")

        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(pizza)
        )
