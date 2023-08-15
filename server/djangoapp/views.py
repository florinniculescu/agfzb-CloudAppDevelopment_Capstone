from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# for static pages
from django.views.generic import TemplateView
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.template import RequestContext
import random


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

#commented as the example wants to use a function
#class AboutPageView(TemplateView):
#    template_name = 'about.html'
#class ContactPageView(TemplateView):
#    template_name = 'contact.html'
# Create an `about` view to render a static about page

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/3c122bad-f41e-4e17-bcbd-be4f913886e7/dealerships/get_all_dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = dict()
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealership_list(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/dealerships.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/3c122bad-f41e-4e17-bcbd-be4f913886e7/dealerships/get_reviews_per_dealership"
        # Get reviewers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all reviewer's name
        reviewer_names_sentiment = ' '.join([reviewer.name + reviewer.sentiment for reviewer in reviews])
        context = dict()
        context["reviews"] = reviews
        context["dealership"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)
        # Return a list of reviewers name
        # return HttpResponse(reviewer_names_sentiment)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # check if user is authentificated is already done in the called from page
    if request.method == "GET":
        context = dict()
        context["dealer_id"] = dealer_id
        # load cars from admin data
        cars = CarModel.objects.filter(Dealer_id = dealer_id)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        print(request)
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/3c122bad-f41e-4e17-bcbd-be4f913886e7/dealerships/add_review_for_dealership"
        review = dict()
        review["id"] = random.randint(1,500)
        review["name"] = request.user.first_name
        review["dealership"] = dealer_id
        review["review"] = request.POST["content"]
        review["purchase"] = request.POST["purchased"]
        review["purchase_date"] = request.POST["purchasedate"]
        # car_id will not be passed
        car_id = str()
        car_id,review["car_make"],review["car_model"],review["car_year"] = request.POST.get('car',None).split('-')
        #review["time"] = datetime.utcnow().isoformat()
        json_payload = dict()
        json_payload["doc"] = review
        json_payload["overwrite"] = True
        post_response = post_request(url, json_payload)
        print(post_response)
        return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details', args=(dealer_id,)))

