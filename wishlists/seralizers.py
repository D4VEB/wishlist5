from django.contrib.auth.models import User
from rest_framework import serializers
from wishlists.models import List, Item, Pledge

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