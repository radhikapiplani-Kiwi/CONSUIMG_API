# create form class
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form class for displaying form  in frontend
    """
    name_of_book = forms.CharField(max_length=20,required=True)
    book_price = forms.CharField(max_length=100,required=True)
    authors_name = forms.CharField(max_length=20,required=True)
    author_phone = forms.CharField(max_length=20,required=True)

    class Meta:
        """
        Meta class for defining behaviour of class
        """
        model = Book
        fields = ('name_of_book', 'book_price', 'authors_name', 'author_phone')