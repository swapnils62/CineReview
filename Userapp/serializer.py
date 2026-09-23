from rest_framework import serializers
from django.contrib.auth.models import User

from Adminapp.models import Movie

from .models import Watchlist
from Reviewapp.models import Reportreview


class Signupserializer(serializers.ModelSerializer):
    first_name=serializers.CharField(write_only=True)
    last_name=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True, min_length=8)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password','confirm_password']

    def validate(self, data):
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError('Password and Conform password not match')
        return data

    def validate_username(self,value):
        user=User.objects.filter(username__iexact=value)
        if user.exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_active=False
        )
        return user

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name',]

    def validate_username(self, value):
        users = User.objects.filter(username__iexact=value)
        if self.instance:
            users = users.exclude(pk=self.instance.pk)
        if users.exists():
            raise serializers.ValidationError("This username is already taken.")
        return value


class Movieserialzier(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields=['id','Title','Poster','Released_date']

class Watchlistserailizer(serializers.ModelSerializer):
    movie=Movieserialzier(read_only=True)
    class Meta:
        model=Watchlist
        fields = ['id', 'movie', 'created_at']
    

class Resportserializr(serializers.ModelSerializer):
    class Meta:
        model=Reportreview
        fields=['id','reason',"reasoncategorie","reported_review","report_user","created_at",'status']
        read_only_fields=["reported_review","report_user","status"]