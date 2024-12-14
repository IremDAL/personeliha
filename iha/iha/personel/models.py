import json
from django.db import models


class personeladd(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    
class partsadd(models.Model):
    Id = models.AutoField(primary_key=True)
    team = models.CharField(max_length=50)
    aircraft = models.CharField(max_length=50)
    parts = models.CharField(max_length=50)
    isDeleted = models.BooleanField(default=False)
    def __str__(self):
        return self.parts
class ucakparcasayilari(models.Model):
    Id = models.AutoField(primary_key=True)
    ucak_adi = models.CharField(max_length=50, unique=True)
    kanat_sayisi = models.IntegerField(default=0)
    kuyruk_sayisi = models.IntegerField(default=0)
    govde_sayisi = models.IntegerField(default=0)
    aviyonik_sayisi = models.IntegerField(default=0)

    def __str__(self):
        return self.ucak_adi
class ucaklar(models.Model):
    Id = models.AutoField(primary_key=True)
    aircraft = models.CharField(max_length=50)
    partss = models.TextField(default='[]')  

    def __str__(self):
        return self.aircraft