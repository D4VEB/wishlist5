import stripe
from django.contrib.auth.models import User
from stripe import Charge
from wishlists.models import List, Item, Pledge, Profile
from rest_framework import serializers


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        user = serializers.ReadOnlyField(source='user.id')
        fields = ('id', 'title', 'user', 'created_at', 'modified_at',
                  'deadline', 'expired',)
        read_only_fields = ('user', 'created_at', 'modified_at', 'expired',)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'list', 'image','description', 'price',
                  'created_at','modified_at')
        read_only_fields = ('dollars_pledged', 'created_at', 'modified_at')


class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        user = serializers.ReadOnlyField(source='user.id')
        fields = ('user', 'item', 'pledge_value', 'created_at', 'modified_at')
        read_only_fields = ('user', 'created_at', 'modified_at')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'id', 'email', 'shipping_address')
        read_only_fields = ('user', 'id')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# see this thread... http://stackoverflow.com/questions/28736916/django-rest-framework-and-stripe-best-practice

class ChargeSerializer(serializers.Serializer):
    class Meta:
        model = Charge
        fields = '__all__'

    def create(self, validated_data):
        charge = Charge.objects.create(**validated_data)

        # Will raise an Excetpion and stop the creation:
        response = stripe.Charge.create(
            amount=charge.cost,
            currency="usd",
            source=validated_data["token"],
            description="Charge"
        )
        return charge