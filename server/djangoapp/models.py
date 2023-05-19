from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    NAME = 'Name'
    DESC = 'Description'
    def __str__(self):
        return "Name: " + self.NAME + ", " + \
                "Description: " + self.DESC

class CarModel(models.Model):
    Carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    Dealer_id = models.IntegerField(null=False, max_length=2, default=0)
    Name = 'Name'
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
        return "Car Make: " + self.Carmake + ", " + \
                "Dealer_id: " + self.Dealer_id + ", " \
                "Name: " + str(self.Name) + ", " + \
                "Type: " + self.Type + ", " + \
                "Year: " + self.str(self.Year)
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
