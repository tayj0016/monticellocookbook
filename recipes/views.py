from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
from django.views import View
from .forms import RecipeForm, CommentForm
from .models import Recipe, Comment, Category

import requests
from . import scrape


class RecipeIndexView(TemplateView):
    template_name = 'recipes/recipe_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        return context


# Generic class-based view for index
# Uses recipe_list.html as default template, unless otherwise specified
class RecipeListView(ListView):
    queryset = Recipe.objects.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        return context


# Generic class-based view for displaying recipe details
class RecipeView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])

    def get_queryset(self):
        return Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(recipe=self.kwargs['pk']).order_by('created_at')
        context['category_list'] = Category.objects.all().order_by('name')
        return context


# function-based view for creating a new recipe using forms
# Check form action attr and header navbar
@login_required(login_url='/admin/')
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            # recipes_scrape.success()
            recipe = form.save(commit=False)
            url = form.cleaned_data['url']
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            user = request.user
            result = scrape.scrape(url, soup, recipe, user)
            # print(form.cleaned_data.get('url'))
            # print myForm.cleaned_data.get('description')
            if result is True:
                category_list = Category.objects.all().order_by('name')
                return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'category_list': category_list})
            else:
                return redirect('https://www.unf.edu/ecenter')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin/'
    model = Recipe
    template_name = 'recipes/recipe_edit.html'
    fields = ['title', 'description', 'url', 'website']


# Generic class-based view for deleting a recipe
class RecipeDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin/'
    model = Recipe
    success_url = reverse_lazy('recipes:home')


# Generic class-based view for displaying all recipes of a certain category
class CategoryView(ListView):
    model = Category
    template_name = 'recipes/recipe_list.html'

    def get_queryset(self, **kwargs):
        return Recipe.objects.filter(category_id=self.kwargs['pk']).order_by('title')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all().order_by('name')
        return context

# COMMENT VIEWS
# class-based view for adding comments
class CommentView(LoginRequiredMixin, FormView):
    login_url = '/admin/'
    template_name = 'recipes/comment_form.html'
    form_class = CommentForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        comment = form.save(commit=False)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        comment.recipe = recipe
        comment.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        pk = self.kwargs['pk']
        return reverse_lazy('recipes:detail', kwargs={'pk': pk})


class CommentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/admin/'
    model = Comment
    template_name = 'recipes/comment_edit.html'
    fields = ['content']


# Generic class-based view for deleting a recipe
class CommentDelete(LoginRequiredMixin, DeleteView):
    login_url = '/admin/'
    model = Comment

    def get_success_url(self, **kwargs):
        obj = Comment.objects.get(id=self.kwargs['pk'])
        return reverse_lazy('recipes:detail', args=[obj.recipe_id])