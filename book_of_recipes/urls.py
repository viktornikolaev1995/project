from django.urls import path, re_path
from .views import RecipeList, RecipeDetail, RecipeListAtCategory, FilterRecipesAtIngredientsView, \
    SearchRecipeAtItsNameView, CreateCommentAtRecipe

urlpatterns = [
    re_path(r'^$', RecipeList.as_view(), name='recipes'),
    re_path(r'^recipes-at-category/(?P<slug>[\D-]+)/$', RecipeListAtCategory.as_view(), name='recipes_at_category'),
    re_path(r'^recipe/(?P<slug>[\D-]+)/(?P<slug1>[\D-]+)/$', RecipeDetail.as_view(), name='recipe'),
    path('filter-recipes-at-ingredients/', FilterRecipesAtIngredientsView.as_view(),
         name='filter_recipes_at_ingredients'),
    path('search-recipe-at-its-name/', SearchRecipeAtItsNameView.as_view(), name='search_recipe_at_its_name'),
    re_path(r'^create-comment-at-recipe/(\d+)/$', CreateCommentAtRecipe.as_view(), name='create_comment_at_recipe')
]
