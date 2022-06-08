from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
        #Homepage
        path('', views.RecipeIndexView.as_view(), name='home'),

        # RECIPE VIEWS
        # Recipe List view, generic class-based
        path('list/', views.RecipeListView.as_view(), name='list'),

        # RecipeDetail View
        path('<int:pk>/', views.RecipeView.as_view(), name='detail'),

        # Create a new recipe, function-based
        path('new/', views.recipe_new, name='recipe_new'),

        # # Update a recipe, generic class-based
        path('<int:pk>/update', views.RecipeUpdate.as_view(), name='update'),

        # delete a recipe, generic class-based
        path('<int:pk>/delete', views.RecipeDelete.as_view(), name='delete'),

        # List recipes of a category, generic class-based
        path('category/<int:pk>', views.CategoryView.as_view(), name='category'),

        # # Add comment to recipe
        path('<int:pk>/comment', views.CommentView.as_view(), name='comment'),

        # Delete a comment
        path('comment/<int:pk>/delete', views.CommentDelete.as_view(), name='comment_delete'),

        # Update a recipe comment, generic class-based
        path('comment/<int:pk>/update', views.CommentUpdate.as_view(), name='comment_update'),
]
