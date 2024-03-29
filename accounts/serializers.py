from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
	        required=True,
	        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
	        )

	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = CustomUser
		fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'password2']
		extra_kwargs = {
		    'first_name': {'required': True},
		    'last_name': {'required': True},
		    'phone_number' : {'required': True},
		}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
		    raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	def create(self, validated_data):
	    user = CustomUser.objects.create(
	    email = validated_data['email'],
	    first_name = validated_data['first_name'], 
	    last_name = validated_data['last_name'],
	    phone_number = validated_data['phone_number'],
	    )

	    user.set_password(validated_data['password'])
	    user.save()    

	    return user


class CustomUserSerializer(serializers.ModelSerializer):

	class Meta():
		model = CustomUser
		fields = ['email', 'first_name', 'last_name', 'phone_number', 'image']


class ChangePasswordSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)
	old_password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = CustomUser
		fields = ('old_password', 'password', 'password2')

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
		    raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	def validate_old_password(self, value):
		user = self.context['request'].user
		if not user.check_password(value):
			raise serializers.ValidationError({"old_password": "Old password is not correct"})
		return value

	def update(self, instance, validated_data):

		instance.set_password(validated_data['password'])
		instance.save()

		return instance

class UpdateProfileSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ['email', 'first_name', 'last_name', 'phone_number']

	def validate_email(self, value):
		user = self.context['request'].user
		if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
			raise serializers.ValidationError({"email": "This email is already in use."})
		return value

	def validate_phone_number(self, value):
		user = self.context['request'].user
		if CustomUser.objects.exclude(pk=user.pk).filter(phone_number=value).exists():
			raise serializers.ValidationError({"username": "This phone number is already in use."})
		return value

	def update(self, instance, validated_data):

		instance.first_name = validated_data['first_name']
		instance.last_name = validated_data['last_name']
		instance.email = validated_data['email']
		instance.phone_number = validated_data['phone_number']

		instance.save()

		return instance