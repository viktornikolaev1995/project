from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class CommonInfo(models.Model):
    """Общая информация"""
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True)
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(CommonInfo):
    """Категория рецептов"""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Recipe(CommonInfo):
    """Рецепт"""

    image = models.ImageField(upload_to='recipes/%Y/%m/%d/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='recipes',
        related_query_name='recipe',
        blank=True,
        null=True
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    cooking_time = models.CharField(max_length=100, verbose_name='Время приготовления')
    user = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        related_name='recipes',
        related_query_name='recipe',
        blank=True,
        null=True
    )
    archive = models.BooleanField(default=False, verbose_name='Архив')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.category.slug, 'slug1': self.slug})


class Ingredient(CommonInfo):
    """Ингредиент"""
    KILOGRAM = 'кг'
    GRAM = 'г'
    LITRE = 'л'
    MILLILITRE = 'мл'
    PIECE = 'шт.'
    TABLESPOON = 'ст.л.'
    TEASPOON = 'ч.л.'

    UNIT_OF_MEASUREMENT_CHOICES = [
        (KILOGRAM, 'кг'),
        (GRAM, 'г'),
        (LITRE, 'л'),
        (MILLILITRE, 'мл'),
        (PIECE, 'шт.'),
        (TABLESPOON, 'ст.л.'),
        (TEASPOON, 'ч.л.'),
    ]

    quantity = models.CharField(max_length=50, verbose_name='Количество', blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=10, choices=UNIT_OF_MEASUREMENT_CHOICES,
                                           verbose_name='Единица измерения', blank=True, null=True)

    def clean(self):
        """
        Checks, that we do not create multiple ingredients with
        no quantity and the same name of ingredient.
        """
        if self.quantity is None and Ingredient.objects.filter(name=self.name, quantity__isnull=True).exists():
            raise ValidationError("Another Ingredient with name=%s and no quantity already exists" % self.name)

    def __str__(self):
        if self.quantity and self.unit_of_measurement:
            return f'{self.name}-{self.quantity}-{self.unit_of_measurement}'
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        unique_together = ['name', 'quantity', 'unit_of_measurement']


class StepCookingAtRecipe(CommonInfo):
    """Шаг приготовления по рецепту"""

    image = models.ImageField(upload_to='images_of_steps_for_cooking_at_recipe/%Y/%m/%d/', verbose_name='Изображение',
                              blank=True, null=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='steps_cooking_at_recipe',
        related_query_name='step_cooking_at_recipe',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Шаг приготовления по рецепту'
        verbose_name_plural = 'Шаги приготовления по рецепту'


class RecipeComments(MPTTModel):
    """Комментарии к рецепту"""

    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(max_length=1000, verbose_name='Текст комментария')
    email = models.EmailField(verbose_name='Почта')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания комментария')
    parent = TreeForeignKey(
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
        related_name='recipe_comments',
        related_query_name='recipe_comment',
    )

    def __str__(self):
        return f'{self.name}-{self.recipe}'

    class Meta:
        verbose_name = 'Комментарий к рецепту'
        verbose_name_plural = 'Комментарии к рецепту'

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['parent', 'pub_date']
