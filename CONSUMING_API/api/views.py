from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework import status
from .models import Book
from .serializer import  CreateBookSerializer,UpdateBookSerializer
from .form import BookForm
from.constants import *
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book

    def get_serializer_class(self):
        """
        Get the Serializer Class as CreateBookSerializer or UpdateBookSerializer as per required action
        """
        if self.action == ['list', 'create']:
            return CreateBookSerializer
        else:
            return UpdateBookSerializer

    def get_queryset(self, pk=None):
        """
        Get the queryset of Book Model
        """
        return Book.objects.filter().order_by('id')

    def list(self, request, *args, **kwargs):
        """
        list all the Books Data

        """
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves an instance of Book Model
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create new Book instance with Books Data
        """

        serializer = CreateBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Updates the instance with its new values
        """
        ins = self.get_object()
        serializer = self.get_serializer(ins, data=request.data)
        if serializer.is_valid():
            serializer.update(ins, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': MESSAGE_1}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates the instance with its new values
        """
        ins = self.get_object()
        serializer = self.get_serializer(ins, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(ins, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': MESSAGE_2}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an instance of Book
        """
        data = self.get_object()
        data.delete()
        return Response({'msg': MESSAGE_3})


def add_books(request):
    """
    render a form to store data through API
    :param request:request user
    :return: form template
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            response = requests.post(BASIC_URL, data=form.data)
            if response.status_code == 201:
                book = response.json()
            return redirect('show')
    else:
        form = BookForm()
    return render(request, 'form.html', {'form': form})

def show_books(request):
    """
    show the books details through consuming API
    :param request:request user
    :return: show template
    """
    response = requests.get(BASIC_URL)
    book = response.json()
    return render(request, 'show.html', {'book': book})

def retrieve_books(request, pk):
    """
    retrieve an instance of Book
    :param request:request user
    :param pk: id of an instance
    :return: retrieve template
    """
    response =requests.get(f'{BASIC_URL}/{pk}/')
    book = response.json()
    return render(request, 'retrieve.html', {'book': book})

def update_books(request, pk):
    """
    update the instance of book through API
    :param request:request user
    :param pk: id of an instance
    :return: update template
    """
    response = requests.get(f'{BASIC_URL}/{pk}/')
    data = response.json()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            data = {'name_of_book': form.cleaned_data['name_of_book'],
                    'book_price': form.cleaned_data['book_price'],
                    'authors_name': form.cleaned_data['authors_name'],
                    'author_phone': form.cleaned_data['author_phone'],
                    }
            response = requests.put(f'{BASIC_URL}/{pk}/', data=data)
            if response.status_code == 201:
                return redirect('show')
            else:
                return render(request, 'update.html')
    else:
        form = BookForm(initial=data)
    return render(request, 'update.html', {'form': form})

def delete_books(request, pk):
    """
    delete an instance of book
    :param request:request user
    :param pk: id of an instance
    :return: redirect user to show template after deleting the selected template
    """
    url =f'{BASIC_URL}/{pk}/'
    response = requests.delete(url)
    return redirect('show')