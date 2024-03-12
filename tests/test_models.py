from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import Dish, DishType, Cook


class DishTypeTest(TestCase):
    def test_dish_type_str_method(self) -> None:
        dish_type = DishType.objects.create(
            name="pizza",
        )

        self.assertEqual(str(dish_type), "pizza")


class CookTest(TestCase):
    def test_cook_str_method(self) -> None:
        cook = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            first_name="test_first_name",
            last_name="test_last_name",
            years_of_cooking=8
        )

        self.assertEqual(
            str(cook),
            "test_username (test_first_name test_last_name)"
        )


class DishTest(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(
            name="sushi",
        )

    def test_dish_str_method(self) -> None:
        dish = Dish.objects.create(
            name="test_dish",
            price=20.1,
            dish_type=self.dish_type,
        )

        self.assertEqual(str(dish), "test_dish (20.1)")
