from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
  """
  This class defines the filters for the Product model.

  Attributes:
    collection_id (int): The primary key for the collection.
    unit_price (decimal): The unit price of the product.
  """
  class Meta:
    model = Product
    fields = {
      'collection_id': ['exact'],
      'unit_price': ['gt', 'lt']
    }