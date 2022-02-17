from django.urls import path, re_path
from .views import RecipeList, RecipeDetail, RecipeListAtCategory

urlpatterns = [
    re_path(r'^$', RecipeList.as_view(), name='recipes'),
    re_path(r'^recipes_at_category/(?P<slug>[\D-]+)/$', RecipeListAtCategory.as_view(), name='recipes_at_category'),
    re_path(r'^recipe/(?P<slug>[\D-]+)/(?P<slug1>[\D-]+)/$', RecipeDetail.as_view(), name='recipe'),

]
