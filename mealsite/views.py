from django.shortcuts import render
from django.views import generic
from django.db.models import Avg
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
import datetime

from .models import Meal
from .forms import MealForm, MealRatingForm
# Create your views here.

class IndexView(generic.ListView, generic.FormView):
    model = Meal
    form_class = MealForm
    success_url = None
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topRate"] = Meal.objects.all().annotate(avg_rating = Avg("mealrating__rating")).filter(avg_rating__gte=3.5).order_by('-avg_rating')[0:3]
        context["Recently"] = Meal.objects.all().order_by('-dateAdded')[0:3]
        return context

    def form_valid(self, form):
        form.save()
        self.success_url = reverse_lazy("meal:index")
        return super().form_valid(form)


class MealListView(generic.ListView):
    model = Meal
    template_name = "mealsite/categoryList.html"
    context_object_name = "meals"

    def get_queryset(self):
        if self.kwargs["category"] == "morning":
            meals = self.model.objects.filter(typicalMealTime=1)
        elif self.kwargs["category"] == "afternoon":
            meals = self.model.objects.filter(typicalMealTime=2)
        elif self.kwargs["category"] == "evening":
            meals = self.model.objects.filter(typicalMealTime=3)
        elif self.kwargs["category"] == "recently":
            now = make_aware(datetime.datetime.now())
            borderElapsedDays = now + datetime.timedelta(days=-3000)
            meals = self.model.objects.all().filter(dateAdded__gte=borderElapsedDays)
        elif self.kwargs["category"] == 'topRate':
            borderRating = 3.5
            meals = self.model.objects.all().annotate(avg_rating = Avg("mealrating__rating")).filter(avg_rating__gte=borderRating)

        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        if q == "rating":
            meals = meals.annotate(avg_rating=Avg("mealrating__rating")).order_by('-avg_rating')
        elif q == "date":
            meals = meals.order_by("-dateAdded")
        else:
            meals = meals.order_by("countryOfOrigin")
        return meals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        return context



class MealDetailView(generic.DetailView, generic.FormView):
    model = Meal
    form_class = MealRatingForm
    template_name = "mealsite/mealDetail.html"
    success_url = None
    context_object_name = "meal"

    def form_valid(self, form):
        rating = form.save(commit=False)
        meal_id = self.kwargs["pk"]
        rating.meal_id = meal_id
        rating.save()

        self.success_url = reverse_lazy('meal:mealDetail', kwargs={"pk": meal_id})
        return super().form_valid(form)



