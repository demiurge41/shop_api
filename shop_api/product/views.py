#product/views.py
from django.shortcuts import render
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review, Artist
from rest_framework import status
from .serializers import (ProductListSerializer, 
                          ProductDetailSerializer, 
                          CategoryListSerializer, 
                          CategoryDetailSerializer, 
                          ReviewListSerializer, 
                          ReviewDetailSerializer, 
                          ArtistDetailSerializer, 
                          ArtistListSerializer, 
                          ProductReviewSerializer,
                          CategoryValidateSerializer,
                          ProductValidateSerializer,
                          ReviewValidateSerializer,
                          
                          
                          )
from django.db import transaction

from rest_framework.generics import (ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView
                                     )

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ArtistDetailSerializer
        return ArtistListSerializer

class UpdateDestroyAPIView(UpdateModelMixin,
                           DestroyModelMixin,
                           GenericAPIView):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.select_related('artist', 'category').prefetch_related('reviews')
    serializer_class = ProductListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductListSerializer

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductValidateSerializer
        return ProductDetailSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count('product'))
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        return CategoryListSerializer

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CategoryValidateSerializer
        return CategoryDetailSerializer


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidateSerializer
        return ReviewListSerializer

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ReviewValidateSerializer
        return ReviewDetailSerializer
    

class ArtistListAPIView(ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistListSerializer


class ArtistDetailAPIView(RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistDetailSerializer
    lookup_field = 'id'


class ProductReviewListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReviewSerializer






# api_view - (ф-я декоратор)

#-----product-------
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)  
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data) 
    
    elif request.method =='DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method =='PUT':
        serializer = ProductValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        product.title = serializer.validated_data.get('title')
        product.image = serializer.validated_data.get('image')
        product.artist_id = serializer.validated_data.get('artist_id')
        product.year_of_creation = serializer.validated_data.get('year_of_creation')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.is_available = serializer.validated_data.get('is_available')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET', 'POST'])
def product_list_api_view(request):

    if request.method =='GET':    
        products = Product.objects.select_related('artist', 'category').prefetch_related('reviews').all()
        data = ProductListSerializer(products, many=True).data
        return Response(data=data)

    elif request.method =='POST':
        serializer = ProductValidateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title')
        image = serializer.validated_data.get('image')
        artist_id = serializer.validated_data.get('artist_id')
        year_of_creation = serializer.validated_data.get('year_of_creation')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        is_available = serializer.validated_data.get('is_available')
        category_id = serializer.validated_data.get('category_id')

        
        product = Product.objects.create(
            title=title,
            image=image, 
            artist_id=artist_id, 
            year_of_creation=year_of_creation, 
            description=description, 
            price=price, 
            is_available=is_available, 
            category_id=category_id,
        )

        
        product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)




#-----categories-------
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)  
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        category.name = serializer.validated_data.get('name')
        category.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)


    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data) 


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method =='GET':
        category = Category.objects.annotate(products_count=Count('product'))

        data = CategoryListSerializer(category, many=True).data
        return Response(data=data)


    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        name = serializer.validated_data.get('name')

        category = Category.objects.create(
            name=name,
        )

        category.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)



#-----reviews-------
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)  
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)

    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data) 


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewListSerializer(reviews, many=True).data
        return Response(data=data)


    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')
        

        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id,
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)





#-----artist-------
@api_view(['GET'])
def artist_detail_api_view(request, id):
    try:
        artist = Artist.objects.get(id=id)  
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


    data = ArtistDetailSerializer(artist, many=False).data
    return Response(data=data) 


@api_view(['GET'])
def artist_list_api_view(request):
    
    artists = Artist.objects.all()
    data = ArtistListSerializer(artists, many=True).data
    return Response(data=data)


@api_view(['GET'])
def products_reviews_list_api_view(request):
    products = Product.objects.all()
    data = ProductReviewSerializer(products, many=True).data
    return Response(data)