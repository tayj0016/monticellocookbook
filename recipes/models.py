from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=75, null=True)
    img_url = models.URLField(null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Recipe(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=600, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    url = models.URLField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    website = models.CharField(max_length=600, blank=True)
    website_url = models.URLField(blank=True)
    thumb = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content[:20]

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})