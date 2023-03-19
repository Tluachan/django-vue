from django.db.models import Q
from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer

class ReviewList(APIView):
    def get_object(self, product_slug):
        try:
            return Review.objects.filter(product__slug=product_slug)
        except Review.DoesNotExist:
            raise Http404
    
    def get(self, request, product_slug, format=None):
        reviews = self.get_object(product_slug)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class CreateReview(APIView):
    def post(self, request, product_slug, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            #product = Product.objects.filter(product__slug=product_slug).first()
            #if not product:
                #raise Http404
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data) 

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})