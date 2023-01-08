from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
       required=True, 
       validators=[UniqueValidator(queryset=User.objects.all())]  #burada USER tablosundan sorgula, kontrol et, unique ise kabul et diyoruz.
       )
  # email default required değil, onu değiştirdik, artık zorunlu alan
  # email unique olsun, değilse validation error dönsün onun için ekledik ve yukarıda import ettik 
  # (UniqueValidator)  

    password = serializers.CharField(
        write_only = True,   # write_only sadece POST, PUT için kullan, GET(yani read) yapılırsa kullanma
        required = True,
        validators = [validate_password],  #djangonun arka planda passwordu valide ettiği yer
        style = {"input_type" : "password"}
    )
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {"input_type" : "password"}
    )
    
    class Meta:
        model = User
        fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'password2'] 

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"message" : "Password fields didnt match!"}
            )
        return data

    def create(self, validated_data):    #? ModelSerializer kullanınca create metodu yazmaya gerek yok aslında fakat, User model içinde olmayan bir field (password2) kullandığımız için creat metodunu override etmek gerekli;
        password = validated_data.get("password")        #passwordu bir değişkene aldım
        validated_data.pop("password2")                  #password2'yi çıkarttım
        user = User.objects.create(**validated_data)     #kalan datayı orm komutuyla user create ediyorum. ilgili fieldları tek tek  eşleştirip map ettik (**validated_data) ile
        user.set_password(password)
        user.save()
        return user

class UserTokenSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")

class CustomTokenSerializer(TokenSerializer):
    user = UserTokenSerailizer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")       