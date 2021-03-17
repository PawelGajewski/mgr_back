from rest_framework import serializers


class znakserializer(serializers.Serializer):
    rodzaj = serializers.CharField(max_length=30)
    symbol = serializers.CharField(max_length=8)
    grafika = serializers.CharField(max_length=255)
    opis = serializers.CharField(max_length=255)


class userserializer(serializers.Serializer):
    nick = serializers.CharField(max_length=20)
    haslo = serializers.CharField(max_length=50)
