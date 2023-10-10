from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entree, name="entree"),
    path('search/', views.search, name="search"),
    path('CreateNewPage/', views.new_page, name="newPage"),
    path('EditPage/<str:title>', views.edit_page, name="EditPage"),
    path('random', views.randomPage, name="randomPage"),
]
