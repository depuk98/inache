import json
from lib2to3.pgen2 import token
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from accounts.models import BaseUserModel, Company, Factory
from accounts.serializers import BaseUserModelSerializer

client = Client()


password = "mypassword"

# my_admin = BaseUserModel.objects.create_superuser('myemail@test.com', password)

# # c = Client()

# You'll need to log him in before you can send requests through the client
lg = client.login(email="myemail@test.com", password=password)

print(lg, "sdsdsdsd")
# register admin user
class registerAdmin(TestCase):
    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        response = client.post(
            reverse("registeradmin"),
            {
                "user_name": "admin",
                "password": password,
                "password2": password,
                "email": "admin@inache.com",
                "Company": com.id,
                "Factory": fac.id,
            },
        )
        print(response.data, "sdsdsd")

    def test_login(self):
        response = client.post(
            reverse("token_obtain_pair"),
            {"email": "admin@inache.com", "password": password},
        )
        print(response.data, "snjskansjkanksakj")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllBaseUsersTest(TestCase):
    """Test module for GET all puppies API"""

    token = ""

    def setUp(self):
        company = Company(
            Legalcompanyname="testcom",
            Address="address",
            POC="person",
            Email="email@email.com",
            PhoneNo=2323131,
        )
        company.save()

        com = Company.objects.get(Legalcompanyname="testcom")
        Factory.objects.create(
            Company=com,
            Code=234,
            Location="Delhi",
            # AwrnsPgms='123',
            # ClosedCases='32'
        )
        fac = Factory.objects.get(Code="234")
        response = client.post(
            reverse("registeradmin"),
            {
                "user_name": "admin",
                "password": password,
                "password2": password,
                "email": "admin@inache.com",
                "Company": com.id,
                "Factory": fac.id,
            },
        )

        BaseUserModel.objects.create(
            name="Casper", password="password", date_joined="2020-01-01"
        )

    def test_get_all_puppies(self):
        response = client.post(
            reverse("token_obtain_pair"),
            {"email": "admin@inache.com", "password": password},
        )
        print(response.data)
        token = response.data["access"]
        # get API response
        response = client.get(
            reverse("getbaseusers"), HTTP_AUTHORIZATION="Bearer {}".format(token)
        )
        # get data from db
        puppies = BaseUserModel.objects.all()
        serializer = BaseUserModelSerializer(puppies, many=True)
        # print(type(response.data),type(serializer.data))
        # ser=json.dumps(serializer.data)
        # res=json.dumps(response.data)
        # print(ser,"ser")
        # print(res,"response")
        # print(len(response.data))
        for value in range(0, len(response.data)):
            # print(response.data[value],"profile_picture")
            response.data[value]["profile_picture"] = None
            # del i['profile_picture']
        print(response.data)
        for value in range(0, len(serializer.data)):
            serializer.data[value]["profile_picture"] = None

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
