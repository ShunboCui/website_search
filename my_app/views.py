import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
# Create your views here.
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
BASE_LIST_URL = 'https://ca.indeed.com/jobs?q={}&l=Hamilton%2C+ON'
def home(request):
    return render(request, template_name = 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_LIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    
    soup = BeautifulSoup(data, features = 'html.parser')
    post_listings = soup.find_all('div', {'class': 'jobsearch-SerpJobCard unifiedRow row result'})
    final_postings = []
    if post_listings == []:
        print("No result")

    for post in post_listings:
        post_title = post.find(class_='jobtitle turnstileLink').text
        post_url = 'https://ca.indeed.com'+ post.find('a').get('href')
        print(post_title)
        print(post_url)


        if post.find(class_='salaryText'):
            post_salary = post.find(class_='salaryText').text
        else:
            post_salary = 'N/A'
        print(post_salary)
        

        if post.find(class_='company'):
            post_company = post.find(class_='company')
  

        final_postings.append((post_title, post_url, post_salary))
    
    for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', for_frontend)