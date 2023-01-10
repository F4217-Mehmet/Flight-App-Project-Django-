from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token


from flight.views import FlightView
from flight.views import Flight
from datetime import datetime, date


class FlightTestCase(APITestCase):
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    today = date.today()

    def setUp(self):
        self.factory = APIRequestFactory()
        self.flight = Flight.objects.create(
            flight_number = 'TK3344',
            operation_airlines = 'THY',
            departure_city = 'Malatya',
            arrival_city = 'Adana',
            date_of_departure = f'{self.today}',
            etd = f'{self.current_time}'
        )
        self.user = User.objects.create_user(
            username='admin',
            password='Aa654321*'
        )

        self.token = Token.objects.get(user=self.user)

    def test_flight_list_as_non_auth_user(self):
        request = self.factory.get('/flight/flights/')
        response = FlightView.as_view({'get': 'list'})(request)
        print(response)
        self.assertNotContains(response, 'reservation')
        self.assertEqual(len(response.data), 0)


    def test_flight_list_as_staff_user(self):
        request = self.factory.get('/flight/flights/', HTTP_AUTHORIZATION= f'Token {self.token}')
        self.user.is_staff=True
        self.user.save()
        # force_authenticate(request, user=self.user)  #tokensız şekilde authenticate ettim
        request.user = self.user
        response = FlightView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'reservation')
        self.assertEqual(len(response.data), 1)




    