from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import RecipeCommentForm
from .models import Recipe, RecipeComments
from .utils import DataMixin


class RecipeList(DataMixin, ListView):
    """List of all available recipes"""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context()
        return dict(list(context.items()) + list(user_context.items()))


class RecipeListAtCategory(DataMixin, ListView):
    """List of recipes by defined category"""

    def get_queryset(self, **kwargs):
        return Recipe.objects.select_related('user', 'category').prefetch_related('ingredients').filter(
            archive=False, category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context()
        return dict(list(context.items()) + list(user_context.items()))


class RecipeDetail(DataMixin, DetailView):
    """Detail view by defined recipe"""

    template_name = 'book_of_recipes/recipe_detail.html'
    slug_field = 'slug'
    context_object_name = 'recipe'
    slug_url_kwarg = 'slug1'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_parents_and_child_comments = {
            parent_comment: [child for child in parent_comment.children.all()] for parent_comment in
            RecipeComments.objects.filter(recipe__slug=self.kwargs['slug1'], parent__isnull=True).order_by('id')
        }

        context['recipe_comments'] = recipe_parents_and_child_comments
        user_context = self.get_user_context()
        return dict(list(context.items()) + list(user_context.items()))


class FilterRecipesAtIngredientsView(DataMixin, ListView):
    """Filters recipes by getting part of ingredients from querystring"""

    def get_queryset(self):
        ingredients_from_querystring = set(self.request.GET.getlist('ingredients'))
        recipe_and_ingredients_names = {
            recipe: {ingredient.name for ingredient in recipe.ingredients.all()} for recipe in
            Recipe.objects.select_related('user', 'category').prefetch_related('ingredients').filter(archive=False)}

        """Return recipe, if ingredients_from_querystring intersects with ingredients_names getting from recipe object, 
        and intersection is equal ingredients_from_querystring"""
        recipes = [recipe for recipe, ingredients_names in recipe_and_ingredients_names.items()
                   if ingredients_from_querystring & ingredients_names == ingredients_from_querystring]
        return recipes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context()
        return dict(list(context.items()) + list(user_context.items()))


class SearchRecipeAtItsNameView(RecipeList):
    """Search recipe by getting part of its name from querystring"""

    def get_queryset(self):
        return Recipe.objects.select_related('user', 'category').prefetch_related('ingredients').filter(
            archive=False, name__icontains=self.request.GET.get("search"))


class CreateCommentAtRecipe(View):
    """Adding a comment to a recipe"""

    def post(self, request, pk):
        form = RecipeCommentForm(request.POST)
        recipe = Recipe.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.recipe_id = pk
            form.save()
        return redirect(recipe.get_absolute_url())
