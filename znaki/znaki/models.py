from django.db import models

class znak(models.Model):
    rodzaj = models.CharField(max_length=30)
    symbol = models.CharField(max_length=8)
    grafika = models.CharField(max_length=255)
    opis = models.CharField(max_length=255)


class user(models.Model):
    nick = models.CharField(max_length=20)
    haslo = models.CharField(max_length=50)
