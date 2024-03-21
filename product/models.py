from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100,)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    date_of_manufacture = models.DateField()
    warranty_information = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.product_name

        