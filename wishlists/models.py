from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import date
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class List(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    deadline = models.DateField(date.today)
    expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def close(self):
        self.expired = True

    def __str__(self):
        return "{}".format(self.title)

class Item(models.Model):
    list = models.ForeignKey(List)
    image = models.ImageField(upload_to="item_images/", null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.FloatField()
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

class Pledge(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    pledge_value = models.FloatField()
    pledge_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def refund(self):

    def __str__(self):
        return "{}".format(self.pledge_amount)


