from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория рецептов"""
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Recipe(models.Model):
    """Рецепт"""

    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='recipe_category',
        blank=True,
        null=True
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.CharField(max_length=100, verbose_name='Время приготовления')
    user = models.OneToOneField(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    archive = models.BooleanField(default=False, verbose_name='Архив')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиент"""
    KILOGRAM = 'кг'
    GRAM = 'г'
    LITRE = 'л'
    MILLILITRE = 'мл'
    PIECE = 'шт.'
    TEASPOON = 'ч.л.'

    UNIT_OF_MEASUREMENT_CHOICES = [
        (KILOGRAM, 'кг'),
        (GRAM, 'г'),
        (LITRE, 'л'),
        (MILLILITRE, 'мл'),
        (PIECE, 'шт.'),
        (TEASPOON, 'ч.л.'),
    ]
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    archive = models.BooleanField(default=False, verbose_name='Архив')
    quantity = models.CharField(max_length=50, verbose_name='Количество', blank=True, null=True)

    unit_of_measurement = models.CharField(
        max_length=10,
        choices=UNIT_OF_MEASUREMENT_CHOICES,
        verbose_name='Единица измерения',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name}-{self.quantity}-{self.unit_of_measurement}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class StepCookingAtRecipe(models.Model):
    """Шаг приготовления по рецепту"""

    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='images_of_steps_for_cooking_at_recipe/%Y/%m/%d/', verbose_name='Изображение',
                              blank=True, null=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='steps_for_cooking_at_recipe',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шаг приготовления по рецепту'
        verbose_name_plural = 'Шаги приготовления по рецепту'


class RecipeComments(models.Model):
    """Комментарии к рецепту"""

    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(max_length=2500, verbose_name='Текст отзыва')
    email = models.EmailField(verbose_name='Почта')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания отзыва')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name="Родитель",
        related_name="children",
        blank=True,
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_review'
    )

    def get_all_children(self):
        return RecipeComments.objects.filter(parent_id=self.pk).order_by('id')

    def __str__(self):
        return f'{self.name}-{self.recipe}'

    class Meta:
        verbose_name = 'Комментарий к рецепту'
        verbose_name_plural = 'Комментарии к рецепту'
