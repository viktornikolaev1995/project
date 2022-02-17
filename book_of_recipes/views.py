from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe


class RecipeList(ListView):
    model = Recipe
    template_name = 'book_of_recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        obj = Recipe.objects.all()
        if obj.exists():
            return obj

        # raise Http404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецепты'
        return context
