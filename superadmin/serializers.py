from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'username', 'name', 'email_address', 'password', 'mobile_number', 'date_joined','status']
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return Admin.objects.create(**validated_data)
    
    
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'plan_name', 'duration' ]
        
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'username', 'name', 'email', 'password', 'mobile_number', 'date_joined','status','staff_role']
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return Staff.objects.create(**validated_data)
    