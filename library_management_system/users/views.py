from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
# Create your views here.

class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        username = request.data['email']
        password = request.data['password']
        user = authenticate(
            username=username, password=password)
        
        refresh = RefreshToken.for_user(user)
        return Response(
            {
               'refresh':str(refresh),
               'access':str(refresh.access_token) 
            }
        )
    
class UserView(APIView):
    def get(self, request):
        #token = request.COOKIES.get('jwt')
        #print(request.headers)
        token = request.headers.get('Authorization')
        token = token.split('Bearer ')[1] 
        print("Hi",token)
        try:
            # Decode the token
            decoded_token = AccessToken(token)
            
            # Extract payload data
            payload = {
                'user_id': decoded_token.payload['user_id'],  # Example: extracting user ID
                'exp': decoded_token.payload['exp'],  # Example: extracting expiry time
                # Add more fields as needed
            }
            print(payload['user_id'])
            return Response(payload, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle decoding errors
            return Response({"error": f"Failed to decode token: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    