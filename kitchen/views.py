from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.models import Dish, DishType, Cook
from kitchen.forms import DishTypeSearchForm, CookSearchForm, CookCreationForm, CookExperienceUpdateForm, \
    DishSearchForm, DishForm


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = get_user_model().objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types
    }

    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5
    context_object_name = "dish_type_list"

    def get_queryset(self, *args, **kwargs):
        name = self.request.GET.get("name")
        queryset = super().get_queryset()

        if name:
            return queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        return context


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_confirm_delete.html"


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        username = self.request.GET.get("username", "")
        queryset = super().get_queryset()

        if username:
            return queryset.filter(username__icontains=username)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        return context


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = get_user_model().objects.prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        name = self.request.GET.get("name")
        queryset = Dish.objects.select_related("dish_type")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = DishSearchForm(initial={"name": name})
        return context


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
