import stripe
from django.contrib.auth.models import User
from wishlists.models import List, Item, Pledge, Profile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    lists = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'lists', 'items', 'profile', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ListSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = List
        fields = '__all__'
        read_only_fields = ('expired')

class ItemSerializer(serializers.ModelSerializer):
    list = ListSerializer(read_only=True)
    pledges = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('dollars_pledged')


class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        user = UserSerializer(read_only=True)
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


# see this thread... http://stackoverflow.com/questions/28736916/django-rest-framework-and-stripe-best-practice

# class ChargeSerializer(serializers.Serializer):
#     class Meta:
#         model = Charge
#         fields = '__all__'
#
#     def create(self, validated_data):
#         charge = Charge.objects.create(**validated_data)
#
#         # Will raise an Excetpion and stop the creation:
#         response = stripe.Charge.create(
#             amount=charge.cost,
#             currency="usd",
#             source=validated_data["token"],
#             description="Charge"
#         )
#         return charge