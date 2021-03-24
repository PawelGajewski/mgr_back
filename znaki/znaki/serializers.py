from rest_framework import serializers
from .models import Znak


class znakserializer(serializers.ModelSerializer):
    rodzaj = serializers.CharField(max_length=30)
    symbol = serializers.CharField(max_length=8)
    grafika = serializers.CharField(max_length=255)
    opis = serializers.CharField(max_length=255)

    class Meta:
        model = Znak
        fields = '__all__'


class userserializer(serializers.ModelSerializer):
    nick = serializers.CharField(max_length=20)
    haslo = serializers.CharField(max_length=50)
