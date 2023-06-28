import threading
from django.shortcuts import render
from myapp.models import MyUser, Product
from myapp.serializers import MyUserSerializer, ProductSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination
from myapp.permissions import IsAdminorReadOnly, IsOwnerorReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    


class HandleEmail(threading.Thread):
    def __init__(self, subject, message, sender, recipient_list):
        self.subject = subject
        self.message = message
        self.sender = sender
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)


    def run(self):
        send_mail(self.subject, self.message, self.sender, self.recipient_list, fail_silently=False)


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsAuthenticated, IsAdminorReadOnly]


class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login was successfull"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Create an account first"}, status=status.HTTP_403_FORBIDDEN)
        

class LogoutApiView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout was successfull"})

        



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerorReadOnly]
    throttle_scope = 'products'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            
            # Sending email to subscribed users every time a product is created 
            """ name = serializer.validated_data['name']
            description = serializer.validated_data['description']
            HandleEmail("New Product Alert: " + name, description, settings.EMAIL_HOST_USER, ['*****@gmail.com']) """

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    