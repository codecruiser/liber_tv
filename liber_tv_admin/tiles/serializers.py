from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Series, Category, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'


class SeriesSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, required=False)
    tags_list = TagSerializer(many=True, required=False)

    class Meta:
        model = Series
        fields = ['name', 'description', 'address', 'categories', 'tags_list', 'position', 'parent']
