from rest_framework import serializers
from .models import *

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = csvdata
        fields = '__all__'