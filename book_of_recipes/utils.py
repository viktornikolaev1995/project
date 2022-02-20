from .models import Recipe, Category


class DataMixin:
    """Common info for views"""
    model = Recipe
    template_name = 'book_of_recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.select_related('user', 'category').prefetch_related('ingredients').filter(archive=False)

    def get_user_context(self, **kwargs):
        context = kwargs
        context['categories'] = Category.objects.all()
        context['ingredients'] = sorted(list(
            {
                ingredient.name for recipe in Recipe.objects.prefetch_related('ingredients').filter(archive=False)
                for ingredient in recipe.ingredients.all()
            }))

        return context
