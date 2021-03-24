from django.db import models

class Znak(models.Model):
    rodzaj = models.CharField(max_length=30)
    symbol = models.CharField(max_length=8)
    grafika = models.CharField(max_length=255)
    opis = models.CharField(max_length=255)


class User(models.Model):
    nick = models.CharField(max_length=20)
    haslo = models.CharField(max_length=50)
