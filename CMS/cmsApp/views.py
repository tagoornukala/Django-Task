from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics
from rest_framework.views import APIView

# Create your views here.

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password = serializer.validated_data['password'])
            if user is not None:
                token,created = Token.objects.get_or_create(user=user)
                return Response({'token':token.key})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        token = Token.objects.filter(user=request.user)
        token.delete()
        return Response({'message':"logout successfully"})


class Userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializer

class Postviewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = Postserializer
    # permission_classes = [IsAuthenticated]
    


class Likeviewset(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = Likeserializer
    # permission_classes = [IsAuthenticated]
