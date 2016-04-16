import os
from wishlists.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from django.conf import settings
from django.contrib.auth.models import User
from wishlists.models import List, Item, Pledge, Profile
from rest_framework import generics
from rest_framework.serializers import ListSerializer
from wishlists.seralizers import ListSerializer, ItemSerializer, \
        PledgeSerializer, ProfileSerializer, UserSerializer #, #ChargeSerializer
import stripe

class ListCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListCreateList(generics.ListCreateAPIView):
    queryset = List.objects.order_by('-created_at')
    serializer_class = ListSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class DetailUpdateDeleteList(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ListCreateItem(generics.ListCreateAPIView):
    queryset = Item.objects.order_by('-created_at')
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(list=self.request.list)

class DetailUpdateDeleteItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ListCreatePledge(generics.ListCreateAPIView):
    queryset = Pledge.objects.order_by('-created_at')
    serializer_class = PledgeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(item=self.request.item)
        serializer.save(user=self.request.user)

        stripe.api_key = os.environ('STRIPE_API_KEY')
        token = serializer.initial_data['token']

        token = self.request.POST["stripeToken"]

        stripe.api_key = settings.STRIPE_SECRET_KEY

        amount = int(float(self.request.POST['amount']) * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,  # amount in cents, again
                currency="usd",
                source=token,
                description="Pledge submitted"
            )
        except stripe.error.CardError as e:
            # need to add a response to error here...
            pass

class DetailUpdateDeletePledge(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ListCreateProfile(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class DetailUpdateProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# class MakePledge(generics.CreateAPIView):
#     serializer_class = ChargeSerializer

    # def pledge_transaction(request):
    #
    #     # Set your secret key: remember to change this to your live secret key in production
    #     # See your keys here https://dashboard.stripe.com/account/apikeys
    #     stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"
    #
    #     # Get the credit card details submitted by the form
    #     token = request.POST['stripeToken']
    #
    #     # Create the charge on Stripe's servers - this will charge the user's card
    #     try:
    #         charge = stripe.Charge.create(
    #             amount=1000,  # amount in cents, again
    #             currency="usd",
    #             source=token,
    #             description="Example charge"
    #         )
    #     except stripe.error.CardError as e:
    #         # The card has been declined
    #         pass