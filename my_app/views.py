import requests

from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
# to turn spaces into proper url format ++++
from requests.compat import quote_plus

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    response = requests.get(BASE_CRAIGSLIST_URL.format(quote_plus(search)))
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_listings = []
    for post in post_listings:
        # post_title = post.find(class_='result-title').text
        # post_url = post.find('a').get('href')
        # if post.find(class_='result-price'):
        #     post_price = post.find(class_='result-price').text
        # else:
        #     post_price = "N/A"

        # final_listings.append((post_title, post_url, post_price))

        if post.find(class_='result-image').get('data-ids'):
            post_image = BASE_IMAGE_URL.format(post.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1])
        else:
            post_image = 'https://dubsism.files.wordpress.com/2017/12/image-not-found.png'

        final_listings.append(
            (post.find(class_='result-title').text,
             post.find('a').get('href'),
             post.find(class_='result-price').text,
             post_image),
        )

    context_items = {
        'search': search,
        'final_listings': final_listings,
    }
    return render(request, 'my_app/new_search.html', context_items)
