from rest_framework import serializers
from .models import Category, Product, Review, Artist
from django.db.models import Avg
from rest_framework.exceptions import ValidationError


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = 'id name'.split()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']



class ProductListSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer(many=False)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title year_of_creation price artist category reviews'.split()
        depth = 1


    def get_category(self, product):
        return product.category.name if product.category else None
    

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = 'id name products_count'.split()


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ArtistDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = 'id name image description'.split()

class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews', 'avg_rating']

    def get_avg_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('stars'))['avg'] or 0
    

#validate

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,  min_length=2, max_length=100)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255)
    image = serializers.ImageField(required=False, allow_null=True)
    artist_id = serializers.IntegerField(required=False, allow_null=True)
    year_of_creation = serializers.IntegerField()
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_available = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_artist_id(self, artist_id):
        if artist_id is None:
            return artist_id
        try:
            Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            raise ValidationError("Artist doesn't exist")
        return artist_id

    def validate_category_id(self, category_id):
        if category_id is None:
            return category_id
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError("Category doesn't exist")
        return category_id
    
    def validate_year_of_creation(self, year_of_creation):
        if year_of_creation < 0:
            raise ValidationError("Year of creation must be positive")
        return year_of_creation
    
class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    stars = serializers.IntegerField(min_value=1, max_value=10)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product doesn't exist")
        return product_id