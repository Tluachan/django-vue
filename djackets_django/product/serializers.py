from rest_framework import serializers

from .models import Category, Product, Review

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.ReadOnlyField(source='user_id.username')
    shop_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = (
            'id',
            'user_id',
            'shop_id',
            'content',
            'rating',
            'datetime',
            'username'
        )

    def create(self, validated_data):
        # Get the user and product objects from the validated data
        user = self.context["request"].user
        product = self.context["product"]

        # Create the review object with the validated data and user/product objects
        review = Review.objects.create(
            user_id=user.id,
            shop_id=product.id,
            content=validated_data["content"],
            rating=validated_data["rating"],
        )

        return review    

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "address",
            "get_absolute_url",
            "phone",
            "map_url",
            "avg_rating",
            "get_image",
            "get_thumbnail",
            "reviews"
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
            "get_image",
            "get_thumbnail",
        )

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_staff')