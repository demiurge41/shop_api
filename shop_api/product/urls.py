#product/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # categories
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    # products
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('products/reviews/', views.ProductReviewListAPIView.as_view()),

    # reviews
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),

    # artists
    path('artists/', views.ArtistViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('artists/<int:id>/', views.ArtistViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]