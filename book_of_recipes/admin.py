from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe
from .models import Category, Recipe, Ingredient, StepCookingAtRecipe, RecipeComments
from django.forms import TextInput, Textarea, ModelForm
from django.db import models


class RecipeAdminForm(ModelForm):
    ingredients = forms.ModelMultipleChoiceField(label='Ингредиенты',
                                                 widget=FilteredSelectMultiple(verbose_name="name", is_stacked=True,),
                                                 queryset=Ingredient.objects.all().order_by('name'))


class StepCookingAtRecipeInline(admin.TabularInline):
    model = StepCookingAtRecipe
    extra = 1
    readonly_fields = ('get_image',)
    prepopulated_fields = {'slug': ('recipe', 'name')}

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src={obj.image.url} width="100" height="85"')
        else:
            return mark_safe(f'<img src="#"')

    get_image.short_description = 'Изображение'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'get_image', 'user')
    form = RecipeAdminForm
    list_filter = ('category', 'user')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [StepCookingAtRecipeInline]
    readonly_fields = ('get_image',)

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 100})}
    }

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src={obj.image.url} width="100" height="85"')
        else:
            return mark_safe(f'<img src="#"')

    get_image.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    fields = (
        ('name', 'slug'),
        'description',
        ('quantity', 'unit_of_measurement')
    )
    list_filter = ('unit_of_measurement',)
    prepopulated_fields = {'slug': ('name', 'quantity', 'unit_of_measurement')}

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }


@admin.register(StepCookingAtRecipe)
class StepCookingAtRecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'recipe', 'get_image')
    prepopulated_fields = {'slug': ('recipe', 'name')}
    fields = (
        ('name', 'slug', 'recipe', 'image'),
        'description'
    )
    list_filter = ('recipe',)
    readonly_fields = ('get_image',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src={obj.image.url} width="100" height="85"')
        else:
            return mark_safe(f'<img src="#"')

    get_image.short_description = 'Изображение'


@admin.register(RecipeComments)
class RecipeCommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'recipe')
    fields = (
        ('name', 'email'), 'text', ('recipe', 'parent')
    )
    list_filter = ('recipe',)


admin.site.site_title = 'Best Recipes'
admin.site.site_header = 'Best Recipes'
