from rest_framework import serializers
from .models import *


class znakserializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=30)
    symbol = serializers.CharField(max_length=8)
    description = serializers.CharField(max_length=255)

    class Meta:
        model = Znak
        fields = '__all__'


class userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'isAdmin']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RecognitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recognition
        fields = '__all__'


class RecognitionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionGroup
        fields = '__all__'