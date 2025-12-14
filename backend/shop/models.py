# Create your models here.

from django.db import models


# This class represents a Sweet item in our system
# Each sweet will be stored as a row in the database


class Sweet(models.Model):
    
    # Name of the sweet (example: Gulab Jamun, Rasgulla)
    # It must be unique so that the same sweet name is not added twice

    name = models.CharField(max_length=100, unique=True)

    # Category of the sweet (example: Dry Sweet, Milk Sweet, Bengali Sweet)


    category = models.CharField(max_length=50)

    # Price of the sweet (example: 250.50)
    # Decimal is used to handle money values correctly

    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Quantity available in stock
    # Only positive numbers are allowed (no negative quantity)

    quantity = models.PositiveIntegerField()
    
    # Image of the sweet (optional)

    image = models.ImageField(upload_to="sweets/", null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} ({self.quantity})"
