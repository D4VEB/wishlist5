import os
from wishlists.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from wishlists.models import List, Item, Pledge, Profile
from rest_framework import generics, status
from rest_framework.serializers import ListSerializer
from wishlists.seralizers import ListSerializer, ItemSerializer, \
        PledgeSerializer, ProfileSerializer, UserSerializer, ChargeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ListCreateUser(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DetailUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer

class ListCreateList(generics.ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)

class ListAllUsersList(generics.ListAPIView):
    '''
    Front end asked for lists to be sorted by user, but
    but I retained this view in case we want to access lists for
    all users.
    '''
    queryset = List.objects.all()
    serializer_class = ListSerializer


class DetailUpdateDeleteList(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ListCreateItem(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        list_id = self.request.data['list']
        serializer.save(list=List.objects.get(pk=list_id))

class DetailUpdateDeleteItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

class ListPledge(generics.ListAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DetailPledge(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class ListCreateProfile(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class DetailUpdateProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# class TestPayment(ListView):
#     template_name = "wishlists/test_payment_form.html"
#     context_object_name = "items"
#     queryset = List.objects.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = 1
#         context['item'] = 1
#         context['amount'] = 100
#         return context

class CreateCharge(APIView):
    permissions_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):
        serializer = ChargeSerializer(data=request.data)
        if seralizer.is_valid():
            serializer.save(user=request.user)
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)