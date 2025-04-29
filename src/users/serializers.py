from rest_framework import serializers
from .models import User, Profile




class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        phone_number = data.get("phone_number")
        if not email and not phone_number:
            raise serializers.ValidationError(
                "Either email or phone number must be provided."
            )
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            password=validated_data['password1'],
        )
        user.save()
        return user
    

class VerifySerializer(serializers.Serializer):
    """
    Serializer for user verification
    """
    identifier = serializers.CharField()  
    verification_code = serializers.CharField()

    def validate(self, data):
        identifier = data.get("identifier")
        verification_code = data.get("verification_code")
        
        if not identifier:
            raise serializers.ValidationError("identifier must be provided.")
        if not verification_code:
            raise serializers.ValidationError("verification_code must be provided.")
            
        # پیدا کردن کاربر بر اساس ایمیل یا شماره تلفن
        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(phone_number=identifier)
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
            
        return data
