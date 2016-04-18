import stripe
from django.contrib.auth.models import User
from wishlists.models import List, Item, Pledge, Profile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    lists = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'lists', 'profile')

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


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class PledgeSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Pledge
        fields = '__all__'

    #def create(self, validated_data):
        # '''
        # # see this thread... http://stackoverflow.com/questions/28736916/django-rest-framework-and-stripe-best-practice
        # '''
        # stripe.api_key = os.environ('STRIPE_API_KEY')
        # token = serializer.initial_data['token']
        #
        # token = self.request.POST["stripeToken"]
        #
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        #
        # amount = int(float(self.request.POST['amount']) * 100)
        #
        # try:
        #     charge = stripe.Charge.create(
        #         amount=pledge_value,  # amount in cents, again
        #         currency="usd",
        #         source=token,
        #         description="Pledge submitted"
        #     )

        #     return Pledge.objects.create(amount=pledge_value, charge_id=charge["id"],
        #                                  user=user, item=item

        # except stripe.error.CardError as e:
        #     # need to add a response to error here...
        #     pass




