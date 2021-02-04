import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
# Create your views here.
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
BASE_LIST_URL = 'https://toronto.craigslist.org/search/jjj?query={}'
def home(request):
    return render(request, template_name = 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_LIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features = 'html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        print(post_title)
        print(post_url)

        if post.find(class_='result-date'):
            post_date = post.find(class_='result-date').text
        else:
            post_date = 'N/A'
        print(post_date)
        

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_date, post_image_url))
    
    for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', for_frontend)