from django.db import models
from django.db.models import Avg

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="artist_photo", null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    
class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="art_photo", null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    year_of_creation = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_avg_rating(self):
        return self.reviews.aggregate(avg=Avg('stars'))['avg'] or 0

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=((i, i  * '*') for i in range(1, 11)))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'Обзор на {self.text}'


