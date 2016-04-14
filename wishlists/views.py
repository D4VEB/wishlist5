import os
#from wishlists import permissions
from wishlists.models import List, Item, Pledge

from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.serializers import ListSerializer

from wishlists.seralizers import ListSerializer, ItemSerializer, PledgeSerializer


class SmallPagination(PageNumberPagination):
    page_size = 50

class APIListCreateList(generics.ListCreateAPIView):
    queryset = List.objects.order_by('-created_at')
    serializer_class = ListSerializer


    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class APIDetailUpdateList(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class APIListCreateItem(generics.ListCreateAPIView):
    queryset = Item.objects.order_by('-created_at')
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save()

class APIDetailUpdateItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class APIListCreatePledge(generics.ListCreateAPIView):
    queryset = Pledge.objects.order_by('-created_at')
    serializer_class = PledgeSerializer
    pagination_class = SmallPagination

class APIDetailUpdatePledge(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

