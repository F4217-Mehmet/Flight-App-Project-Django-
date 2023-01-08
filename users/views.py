from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        data = serializer.data
        data["token"] = token.key
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



# burayı ben yapmıştım token çıkmadı hata aldım ama açıklamalar var. HA BURADA DURSUN!

# from rest_framework.generics import CreateAPIView
# from django.contrib.auth.models import User
# from .serializers import RegisterSerializer
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token

# class RegisterAPI(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer



# def create(self, request, *args, **kwargs):                # register olacak userın datası burada geliyor
#         serializer = self.get_serializer(data=request.data)# serializerdan geçiriyorum
#         serializer.is_valid(raise_exception=True)          # serializer eğer valid ise
#         user = serializer.save()                           #serializerı save et diyorum, userı return ediyor
#         token = Token.objects.get(user=user)               #userımla token tablosundan tokenımı çekiyorum
#         data = serializer.data                             #register olduktan sonra gelen user bilgisini(serializer.data) data değişkenine atadım
#         data["token"] = token.key                          #tokenın keyini alıyorum
#         headers = self.get_success_headers(serializer.data)#buraya çok takılma, pek esprisi yok.
#         return Response(data, status=status.HTTP_201_CREATED, headers=headers)