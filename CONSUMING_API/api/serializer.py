from rest_framework import serializers
from .models import Book


class CreateBookSerializer(serializers.ModelSerializer):
    """
    Serializer class for Creating Book
    """
    name_of_book = serializers.CharField(max_length=20, required=True)
    book_price = serializers.CharField(max_length=100, required=True)
    authors_name = serializers.CharField(max_length=20, required=True)
    author_phone = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = Book

        fields = ['id', 'name_of_book', 'book_price', 'authors_name', 'author_phone']

    def create(self, validated_data):
        """
        creating an instance
        :param validated_data: data to be inserted
        :return: data instance
        """
        user = Book.objects.create(
            name_of_book=validated_data['name_of_book'],
            book_price=validated_data['book_price'],
            authors_name=validated_data['authors_name'],
            author_phone=validated_data['author_phone'],
        )
        return user


class UpdateBookSerializer(serializers.ModelSerializer):
    """
    Serializer class for Updating Book
    """
    name_of_book = serializers.CharField(max_length=20, required=True)
    book_price = serializers.CharField(max_length=100, required=True)
    authors_name = serializers.CharField(max_length=20, required=True)
    author_phone = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = Book

        fields = ['id', 'name_of_book', 'book_price', 'authors_name', 'author_phone']

    def update(self, instance, validated_data):
        """
        updating an instance
        :param instance:old data
        :param validated_data:new data
        :return: updated data instance
        """
        ins = Book.objects.filter(id=instance.id).update(
            name_of_book=validated_data.get('name_of_book'),
            book_price=validated_data.get('book_price'),
            authors_name=validated_data.get('authors_name'),
            author_phone=validated_data.get('author_phone'))
        return ins
