from rest_framework import serializers
from .models import Flight, Reservation, Passenger


class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger   
        fields = "__all__"     

class ReservationSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many=True, required=True)
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ("id", "flight", "flight_id", "user", "passenger")  
        
#frontendden gelen veri database'e serializerdan geçerek kaydedileceğinden passenger ve flight bilgilerini ayırıp sonra başka bir tabloda birleştireceğiz. many to many

    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")  #validated data'da tüm bilgiler mevcut olduğundan bundan passengeri çıkarıp, passenger_data'ya atadım. validated_data'da uçuş bilgileri kaldı. bu  datayı reservation tablosuna kaydedeceğinden user_id bilgisini eklemem gerek. yani o an login olmus, data isteğini atan userı eklemem lazım.
        validated_data["user_id"] = self.context["request"].user.id #bu şekilde istek atan user'a ulaşırım, user_id ekledim
        reservation = Reservation.objects.create(**validated_data)

        for passenger in passenger_data:  #birden çok passenger olabileceği için for ile döndük
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)  #manytomany de ekleme yönetim standart bu şekilde
        
        reservation.save()
        return reservation
