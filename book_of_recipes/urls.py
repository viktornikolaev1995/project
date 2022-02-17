from django.urls import path, re_path
from .views import RecipeList


urlpatterns = [
    re_path(r'^$', RecipeList.as_view(), name='recipes'),
]