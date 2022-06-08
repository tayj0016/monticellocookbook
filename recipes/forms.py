from django import forms
from .models import Recipe, Comment, Category

choices = Category.objects.all().values_list('name', 'name')

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('url', 'category',)
        labels = {
            'url': 'Recipe:',
        }
        widgets = {
            'url': forms.TextInput(attrs={'class': 'form-control',
                                          'placeholder': 'Recipe URL...',
                                          'aria-describedby': 'Recipe URL...'}),
            'category': forms.Select(choices=choices, attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)
