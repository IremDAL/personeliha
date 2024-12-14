from rest_framework import serializers
from personel.models import personeladd,partsadd,ucaklar,ucakparcasayilari

class PersonelSerializer(serializers.ModelSerializer):
    class Meta:
        model=personeladd
        fields=('Id','name','team','username','password')
class PartsSerializer(serializers.ModelSerializer):
    class Meta:
        model=partsadd
        fields=('Id','team','aircraft','parts','isDeleted')
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model=ucaklar
        fields=('Id','aircraft','partss')