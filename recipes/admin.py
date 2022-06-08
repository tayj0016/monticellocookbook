from django.contrib import admin
from .models import Recipe, Comment, Category

myModels = [Recipe, Comment, Category]

admin.site.register(myModels)