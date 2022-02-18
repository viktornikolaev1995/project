from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe, Category


class RecipeList(ListView):
    model = Recipe
    template_name = 'book_of_recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        obj = Recipe.objects.all()
        if obj.exists():
            return obj

        raise Http404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рецепты со всего мира'
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        return context


class RecipeListAtCategory(ListView):
    model = Recipe
    template_name = 'book_of_recipes/recipe_list_at_category.html'
    context_object_name = 'recipes_at_category'

    def get_queryset(self, **kwargs):
        obj = Recipe.objects.filter(category__slug=self.kwargs['slug'])
        if obj.exists():
            return obj
        raise Http404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Рецепты со всего мира в категории {context["recipes_at_category"][0].category.name.capitalize()}'
        context['categories'] = Category.objects.all()
        return context


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'book_of_recipes/recipe_detail.html'
    slug_field = 'slug'
    context_object_name = 'recipe'
    slug_url_kwarg = 'slug1'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{context["recipe"].name.capitalize()}'
        context['categories'] = Category.objects.all()
        return context

