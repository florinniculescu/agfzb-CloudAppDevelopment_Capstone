from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    Name = models.CharField(max_length=20, default="make name")
    Description = models.TextField(default="make description")
    def __str__(self):
        return "Name: " + self.Name + ", " + \
                "Description: " + self.Description

class CarModel(models.Model):
    Carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    Dealer_id = models.IntegerField(null=False, default=0)
    Name = models.CharField(max_length=20, default="model name")
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    Type = models.CharField(
        null=False,
        max_length=10,
        choices=[(SEDAN,'Sedan'),(SUV,'SUV'),(WAGON, 'Wagon')],
        default=SEDAN
    )
    Year = models.DateField(null=True)
    def __str__(self):
        return "Dealer_id: " + str(self.Dealer_id) + ", " + \
                "Name: " + str(self.Name) + ", " + \
                "Type: " + self.Type + ", " + \
                "Year: " + str(self.Year)
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

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date, review,sentiment):
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Dealership
        self.dealership = dealership
        # Id
        self.id = id
        # Name
        self.name = name
        # Purchase
        self.purchase = purchase
        # Purchase date
        self.purchase_date = purchase_date
        # Review
        self.review = review
        # Sentiment
        self.sentiment = sentiment

    def __str__(self):
        return "Reviewer name: " + self.name
