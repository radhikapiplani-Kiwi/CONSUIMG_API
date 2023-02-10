from django.db import models
from django.urls import reverse


class Book(models.Model):
    """
    Book model to store Books data
    """
    name_of_book = models.CharField(max_length=20)
    book_price = models.CharField(max_length=100)
    authors_name = models.CharField(max_length=20)
    author_phone = models.CharField(max_length=20)

    class Meta:
        """
        Meta class defines the behaviour of class
        """
        db_table = 'Books'

    def get_absolute_url(self):
        return reverse('update', args=[str(self.pk)])
