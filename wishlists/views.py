import os

from django.contrib.auth.models import User
from wishlists.models import List, Item, Pledge, Profile
from rest_framework import generics
from rest_framework.serializers import ListSerializer
from wishlists.seralizers import ListSerializer, ItemSerializer, \
        PledgeSerializer, ProfileSerializer, UserSerializer
import stripe


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

    def perform_create(self, serializer):
        stripe.api_key = os.environ('STRIPE_API_KEY')
        token = serializer.initial_data['token']

        try:
            pledge = stripe.Charge.create(
                amount=serializer.initial_data['pledge_value'],
                currency="usd",
                source=token,
                description="Pledge"
            )
            pledge_id = pledge['id']
        except stripe.error.CardError:
            pass
        serializer.save(pledge_id=pledge_id)

class APIDetailUpdatePledge(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

class APIListCreateProfile(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class APIDetailUpdateProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class APIListCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
