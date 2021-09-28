from django.db import models
from django.contrib.auth.models import AbstractUser

class Znak(models.Model):
    type = models.CharField(max_length=30)
    symbol = models.CharField(max_length=8)
    description = models.CharField(max_length=255)

    def as_dict(self):
        return {
            "id": self.id,
        }


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, default="usr")
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)

class RecognizeManager(models.Manager):
    def create_recognize(self, ownerID, datetime, image, predict, probability, algorithm):
        recognize = self.create(ownerID=ownerID, datetime=datetime, image=image, predict=predict,
                                probability=probability, algorithm=algorithm)
        return recognize


class RecognitionGroup(models.Model):
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    label = models.CharField(max_length=255)
    images_amount = models.CharField(max_length=255, default=0)
    probability = models.FloatField(default=0)
    positive_recognized = models.IntegerField(default=0)
    algorithm = models.CharField(max_length=50)
    accuracy = models.FloatField(default=0)


class Recognition(models.Model):
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    label = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    predict = models.CharField(max_length=10)
    original_sign = models.CharField(max_length=10, default="x")
    probability = models.FloatField()
    algorithm = models.CharField(max_length=50)
    groupID = models.ForeignKey(RecognitionGroup, on_delete=models.CASCADE, default=1)
