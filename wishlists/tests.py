from django.core.urlresolvers import reverse
from datetime import datetime
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from wishlists.models import List, Item

# Create your tests here.

class UserTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="TestUser",
                                             email="test@test.com",
                                             password="pa$$word")
        self.url = reverse("api_user_list_create")

    def test_user_create(self):
        data = {"username": "TestUser", "password": "pa$$word",
                "email": "test@test.com"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class ListTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="TestUser",
                                             email="test@test.com",
                                             password="pa$$word")
        self.list = List.objects.create(title="TestList",
                                                 deadline=datetime.now(),
                                                 user=self.user)

        self.url = reverse("api_list_list_create")

    def test_create_list(self):
        token = Token.objects.get(user_id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"title": "TestList", "deadline": "2016-12-31",
                "user": self.user.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(List.objects.count(), 2)

    def test_list_retrieve(self):
        response = self.client.get(self.url, {"pk": self.list.id},
                                   format="json")
        self.assertEqual(response.data[0]["title"], self.list.title)



class ItemTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="TestUser",
                                             email="test@test.com",
                                             password="pa$$word")

        self.list = List.objects.create(title="TestList",
                                                 deadline=datetime.now(),
                                                 user=self.user)

        self.item = Item.objects.create(title="TestItem",
                                                 price=100000.00,
                                                 list=self.list)

        self.url = reverse("api_item_list_create")

    def test_create_item(self):
        token = Token.objects.get(user_id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        data = {"title": "TestTitle", "price": 100000.00, "list": self.list.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)