from rest_framework import serializers

from .models import Benefactor


class BenefactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefactor
        fields = ('experience', 'free_time_per_week', )

    def create(self, validated_data):
        benefactor= Benefactor.objects.create(**validated_data)
        return benefactor
