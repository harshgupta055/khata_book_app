from rest_framework import serializers
from .models import DailyWage

class DailyWageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyWage
        fields = "__all__"