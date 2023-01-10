from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate


from flight.views import FlightView
from flight.views import Flight


class FlightTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.flight = Flight.objects.create(
            flight_number = 'TK3344',
            operation_airlines = 'THY',
            departure_city = 'Malatya',
            arrival_city = 'Adana',
            date_of_departure = '2023-01-11',
            etd = '08:00:00'
        )
        self.user = User.objects.create_user(
            username='admin',
            password='Aa654321*'
        )

    def test_flight_list_as_non_auth_user(self):
        request = self.factory.get('/flight/flights/')
        response = FlightView.as_view({'get': 'list'})(request)
        print(response)
        self.assertNotContains(response, 'reservation')


    def test_flight_list_as_staff_user(self):
        request = self.factory.get('/flight/flights/')
        self.user.is_staff=True
        self.user.save()
        force_authenticate(request, user=self.user)  #tokensız şekilde authenticate ettim
        request.user = self.user
        response = FlightView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'reservation')



    