from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.template.defaultfilters import default_if_none
from django.utils.safestring import mark_safe
from .models import Category, Recipe, Ingredient, StepCookingAtRecipe, RecipeComments
from django.forms import TextInput, Textarea
from django.db import models


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
    list_display = ('name', 'slug', 'description', 'archive')
    fields = (
        ('name', 'slug'),
        'description',
        ('quantity', 'unit_of_measurement', 'archive')
    )
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


admin.site.site_title = 'Best Recipes'
admin.site.site_header = 'Best Recipes'
