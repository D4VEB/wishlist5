from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)

class List(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='lists')
    deadline = models.DateField()
    expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        '''
        There is a command to purge non-funded items from expired
        lists in management -> commands -> expired_lists.py. This
        process is scheduled/automated through Heroku scheduler.
        '''
        return timezone.now().date() > self.deadline


    def __str__(self):
        return "{}".format(self.title)

class Item(models.Model):
    list = models.ForeignKey(List, related_name='items')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_url = models.URLField(null=True, blank = True)
    item_url = models.URLField(null=True, blank = True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)

    @property
    def dollars_pledged(self):
        total_pledges = self.pledge_set.all()
        dollars_pledged_todate = 0
        for pledge in total_pledges:
             dollars_pledged_todate += pledge.pledge_value
        return dollars_pledged_todate

    @property
    def dollars_to_goal(self):
        total_pledges = self.pledge_set.all()
        outstanding_balance = self.price - total_pledges
        return outstanding_balance

    @property
    def funded_item(self):
        return self.dollars_pledged >= self.price


class Pledge(models.Model):
    user = models.ForeignKey(User, related_name='pledges')
    item = models.ForeignKey(Item, related_name='pledges')
    pledge_value = models.FloatField()
    stripe_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.pledge_value)

class Profile(models.Model):
    shipping_address = models.TextField()
    user = models.OneToOneField(User, null=True,
            blank=True, related_name='profile')





