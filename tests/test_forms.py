from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.forms import (
    DishForm,
    CookCreationForm,
    CookExperienceUpdateForm,
)
from kitchen.models import DishType, Cook


class DishFormTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(
            name="pizza",
        )
        self.cook = get_user_model().objects.create_user(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="1test2"
        )

    def test_dish_creation_form(self) -> None:
        form_data = {
            "name": "test_dish",
            "price": 12.2,
            "dish_type": self.dish_type,
            "cooks": get_user_model().objects.all()
        }

        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())


class CookCreationFormTest(TestCase):
    def test_cook_creation_form(self) -> None:
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "years_of_cooking": 5,
            "password1": "user12test",
            "password2": "user12test",
        }

        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CookExperienceUpdateTest(TestCase):
    def test_cook_update_experience(self) -> None:
        form = CookExperienceUpdateForm(data={
            "years_of_cooking": 10
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data,
            {"years_of_cooking": 10}
        )
