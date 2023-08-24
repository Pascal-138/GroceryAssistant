from django.core.validators import MinValueValidator
from django.db import models

from users.models import User



class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX'    
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'    
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов'
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не менее 1 минуты')
        ]
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',

    )

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        # through_fields=('recipe', 'ingredient'),
        verbose_name='Список ингредиентов',
        related_name='recipes',
        )

    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64',
        upload_to='recipes/',
    )

    pub = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub']

    def __str__(self) -> str:
        return self.name
    

class Ingredient(models.Model):
    """Модель ингредиентов."""
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )

    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    """Модель количества ингредиентов для рецепта."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name= 'ingredient_list',
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name= 'ingredient_list',
    )

    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Список ингредиентов'

    def __str__(self) -> str:
        return f'{self.recipe}, {self.ingredient}, {self.amount}'


class ShoppingCart(models.Model):
    """Модель списка покупок ингредиентов."""
    
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',

    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return (f'Пользователь {self.user} добавил {self.recipe}'
                'в список покупок')
    

class Favorite(models.Model):
    """Модель избранных рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',

    )
    
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


    def __str__(self):
        return (f'Пользователь {self.user} добавил {self.recipe} '
                'в избранное')