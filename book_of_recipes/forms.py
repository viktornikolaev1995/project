from django import forms
from .models import RecipeComments


class RecipeCommentForm(forms.ModelForm):
    """Комментарий к рецепту"""

    class Meta:
        model = RecipeComments
        fields = ('name', 'text', 'email')
