import json
import logging
from datetime import datetime
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from .models import CarModel, CarDealer

from django.contrib import messages
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# ...


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# # ...
#         # Try to check if provide credential can be authenticated
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             # If user is valid, call login method to login current user
#             login(request, user)
#             return redirect('onlinecourse:popular_course_list')
#         else:
#             # If not, return to login page again
#             return render(request, 'onlinecourse/user_login.html', context)
#     else:
#         return render(request, 'onlinecourse/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    if request.method== "GET":
        return render(request, 'djangoapp/registration.html', context)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist=True
        except:
            logger.error("New User")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name= first_name, last_name= last_name, password = password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User Already Exists."
            return render(request,'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/ab976013-9832-4500-9db6-94f740cb2a87/default/get_dealership"
        
        dealerships = get_dealers_from_cf(url)
        context= {'dealership_list': dealerships}
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        print(dealerships)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/12c70528-aec7-4b7b-b97e-d1b60cd3da92/default/get-review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        print("get details in views.py")
        context = {
            "reviews":  reviews, 
            "dealer_id": dealer_id
        }

        return render(request, 'djangoapp/dealer_details.html', context)
        # return HttpResponse(context['reviews'])

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/ab976013-9832-4500-9db6-94f740cb2a87/default/get_dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print("***********************")
            print(context["dealer"][0])
            print(context["cars"])
            print("***********************")
            return render(request, 'djangoapp/add_review.html', context)
        
        if request.method == "POST":
            review = dict()
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if(review["purchase"]):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/13d72415-cef6-4d0c-862f-a35729d1b1d0/default/post-review"
            json_payload = { "review": review }
            print("#########################")
            print(json_payload)
            print("#########################")
            post_request(post_url, json_payload, id=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        return redirect("/djangoapp/login")
# ...

