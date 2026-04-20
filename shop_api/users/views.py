#users/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import (RegisterSerializer,  
                          LoginSerializer, 
                          ConfirmSerializer)

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CodeConfirmation
import random
from rest_framework.views import APIView



class AuthAPIView(APIView):
    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )
        
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(username=username,
                                        password=password,
                                        is_active=False
                                        )
        
        code = str(random.randint(100000, 999999))
        CodeConfirmation.objects.create(user=user, 
                                        code=code
                                        )
        
        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 
                'code': code}
                )




class ConfirmAPIView(APIView):
    def post(self, request):

        serializer = ConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors
                            )

        username = serializer.validated_data.get('username')
        code = serializer.validated_data.get('code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'User not found'}
                            )

        try:
            confirmation_code = CodeConfirmation.objects.get(user=user)
        except CodeConfirmation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Confirmation code not found'}
                            )

        if confirmation_code.code != code:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': 'Invalid code'}
                            )


        user.is_active = True
        user.save()
        confirmation_code.delete()

        return Response(status=status.HTTP_200_OK,
                        data={'message': 'User confirmed successfully'}
                        )