from django.urls import path
from .views import *


urlpatterns = [
    path("category/", ListCategoryAPI.as_view(), name="category_list"),
    path("category/<int:pk>/", RetrieveCategoryAPI.as_view(), name="category"),
]