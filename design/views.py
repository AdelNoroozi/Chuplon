from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Category
from .serializers import CategorySerializer
class ListCategoryAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class RetrieveCategoryAPI(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer