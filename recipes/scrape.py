from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
from .forms import RecipeForm
from .models import Recipe, Category

import requests

def scrape(url, soup, recipe, user):
    success = True

    if soup.title:
        title = soup.title.string
        if title.find("-") != -1:
            title = title.rsplit("-")
            recipe.title = title[0]
        elif title.find("|") != -1:
            title = title.rsplit("|")
            print("test")
            recipe.title = title[0]
        else:
            recipe.title = title
    else:
        success = False

    if soup.find("meta", property="og:description"):
        description = soup.find("meta", property="og:description")
        recipe.description = description["content"][:600]
    elif soup.find(attrs={"name": "description"}):
        description = soup.find(attrs={"name": "description"})
        recipe.description = description["content"][:600]
    else:
        recipe.description = "None"

    if soup.find("meta", property="og:site_name"):
        website = soup.find("meta", property="og:site_name")
        recipe.website = website["content"]
    else:
        recipe.website = "Unknown"

    if soup.find("meta", property="og:image"):
        thumb = soup.find("meta", property="og:image")
        recipe.thumb = thumb["content"]
    else:
        recipe.thumb = "https://images.pexels.com/photos/890507/pexels-photo-890507.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260"

    if success is False:
        return False
    else:
        recipe.website_url = url.rsplit(".com")[0] + ".com"
        recipe.author = user
        recipe.save()
        return True
