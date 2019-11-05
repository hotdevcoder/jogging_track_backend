from rest_framework import viewsets

from .models import Entry
from .serializers import EntrySerializer

# Create your views here.
class EntryViewSet(viewsets.ModelViewSet):
  queryset = Entry.objects.all()
  serializer_class = EntrySerializer
