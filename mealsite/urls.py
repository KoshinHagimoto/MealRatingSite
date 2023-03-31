from django.urls import path
from . import views

app_name = 'meal'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/<str:category>/', views.MealListView.as_view(), name="mealList"),
    path('detail/<int:pk>/', views.MealDetailView.as_view(), name="mealDetail")
]