from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name=models.CharField(null=False, max_length=30, default='')
    description = models.CharField(max_length=1000)
    def __str__(self):
        return "Name: "+ self.name + "," + "Description: " + self.description

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarModel(models.Model):
    make= models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer = models.IntegerField()
    name = models.CharField(null=False,max_length=30,default='')
    SEDAN= 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE_CHOICES =[
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    type = models.CharField(null=False, max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField()
    def __str__(self):
        return "Name: "+ self.name+","+"Type: "+self.type

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, lon, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.lon = lon
        self.short_name = short_name
        self.st = st
        self.zip = zip
        
    def __str__(self):
        return "Dealer Name "+self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    def __init__(self, dealership, id, name, purchase, review, purchase_date=None, car_make=None, car_model=None, car_year=None, sentiment="neutral"):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
        
    def __str__(self):
        return "Review : " + self.name