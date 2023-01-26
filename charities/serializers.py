from rest_framework import serializers

from .models import Benefactor
from .models import Charity, Task


class BenefactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefactor
        fields = ('experience', 'free_time_per_week', )

    def create(self, validated_data):
        benefactor= Benefactor.objects.create(**validated_data)
        return benefactor


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('name', 'reg_number')

    def create(self, validated_data):
        charity = Charity.objects.create(**validated_data)
        return charity


class TaskSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(read_only=True, choices=Task.STATE_CHOICES)
    assigned_benefactor = BenefactorSerializer(required=False)
    charity = CharitySerializer(read_only=True)
    charity_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Charity.objects.all(), source='charity')

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'state',
            'charity',
            'charity_id',
            'description',
            'assigned_benefactor',
            'date',
            'age_limit_from',
            'age_limit_to',
            'gender_limit',
        )
