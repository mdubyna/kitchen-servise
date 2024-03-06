from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Dish, DishType, Cook


@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_cooking",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_cooking",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_cooking",
                    )
                },
            ),
        )
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_filter = ("dish_type__name", "cooks")


admin.site.register(DishType)

admin.site.unregister(Group)
