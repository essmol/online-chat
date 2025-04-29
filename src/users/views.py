from rest_framework import generics
from .serializers import UserRegistrationSerializer, VerifySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .utils import send_verification_email, send_verification_sms, redis_client
from django.shortcuts import redirect



class UserRegistrationView(generics.GenericAPIView):
    """
    View for user registration
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification code based on registration method
            if user.email:
                send_verification_email(user.email)
            if user.phone_number:
                send_verification_sms(user.phone_number)
            
            response = Response({
                "message": "Verification code sent",
                "identifier": user.email or user.phone_number
            }, status=status.HTTP_201_CREATED)
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyView(generics.GenericAPIView):
    """
    View for user verification
    """
    serializer_class = VerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        identifier = serializer.validated_data["identifier"]
        user_code = serializer.validated_data["verification_code"]
        
        
        stored_code = redis_client.get(f'verification_code_{identifier}')
        
        if stored_code and stored_code == user_code:
            user = serializer.validated_data['user']
            if '@' in identifier:
                user.is_email_verified = True
            else:
                user.is_phone_verified = True

            user.is_verified = True
            # حذف کد از redis
            redis_client.delete(f'verification_code_{identifier}')
            user.save()
            
            return Response(
                {
                    "user": identifier,
                    "message": "User verified successfully.",
                },
                status=status.HTTP_200_OK,
            )
        
        return Response(
            {"message": "Invalid verification code."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
