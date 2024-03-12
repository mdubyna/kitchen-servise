from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType


URL_COOK_LIST = "kitchen:cook-list"


class PublicCookViewTest(TestCase):
    def test_cook_login_required(self) -> None:
        response = self.client.get(reverse(URL_COOK_LIST))

        self.assertRedirects(
            response,
            "/accounts/login/?next=/cooks/"
        )


class PrivateCookViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
            years_of_cooking=5
        )

        self.client.force_login(self.user)

    def test_cook_correct_template(self) -> None:
        response = self.client.get(reverse(URL_COOK_LIST))

        self.assertEqual(str(response.context["user"]), "test_username ( )")

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_retrieve_cook_list(self) -> None:
        get_user_model().objects.create(
            username="Max",
            password="max123",
            years_of_cooking=4
        )
        get_user_model().objects.create(
            username="Nick",
            password="nick123",
            years_of_cooking=3
        )
        response = self.client.get(reverse(URL_COOK_LIST))
        cooks = get_user_model().objects.all()

        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks)
        )

    def test_cook_list_search(self) -> None:
        get_user_model().objects.create(
            username="Max",
            password="max123",
            years_of_cooking=1
        )
        get_user_model().objects.create(
            username="Nick",
            password="nick123",
            years_of_cooking=2
        )

        response = self.client.get(reverse(URL_COOK_LIST) + "?username=ax")
        cook = get_user_model().objects.filter(username="Max")

        self.assertEqual(
            list(response.context["cook_list"]),
            list(cook)
        )
