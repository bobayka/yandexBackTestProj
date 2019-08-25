from django.db import transaction
from rest_framework import serializers

from marketAnalysis import validators
from marketAnalysis.models import Citizen, Import


class CitizenCreateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(input_formats=["%d.%m.%Y"], validators=[validators.validate_birthday])
    relatives = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        model = Citizen
        fields = ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']


class ImportCreateSerializer(serializers.ModelSerializer):
    citizens = CitizenCreateSerializer(many=True)

    def validate(self, attrs):
        citizens = attrs['citizens']
        citizen_dict = {}
        for data in citizens:
            citizen_id = data['citizen_id']
            if citizen_id in citizen_dict:
                raise serializers.ValidationError(f'Citizen id:{citizen_id} not unique')
            citizen_dict[citizen_id] = data
        for data in citizens:
            citizen_id = data['citizen_id']
            for relative_id in data['relatives']:
                if relative_id not in citizen_dict:
                    raise serializers.ValidationError(f'Relatives with id:{relative_id} doesnt exist')
                is_relative = False
                for id in citizen_dict[relative_id]['relatives']:
                    if id == citizen_id:
                        is_relative = True
                if not is_relative:
                    raise serializers.ValidationError(
                        f'Relatives with id:{relative_id} Relationships are not bilateral')
        return attrs

    def create(self, validated_data):
        imprt = Import.objects.create()
        citizens_data = validated_data.pop('citizens')
        db_citizens = {}
        with transaction.atomic():
            for people in citizens_data:
                relatives = people.pop('relatives')
                db_citizens[people['citizen_id']] = Citizen.objects.create(imports=imprt, **people)
                people['relatives'] = relatives
            for people in citizens_data:
                citizen_id = people['citizen_id']
                citizen = db_citizens[citizen_id]
                for relative in people['relatives']:
                    citizen.relatives.add(db_citizens[relative])

        return imprt

    class Meta:
        model = Import
        fields = ["citizens"]


class MySlugRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        return Citizen.objects.filter(imports_id=self.context['import_id'])


class CitizenUpdateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(input_formats=["%d.%m.%Y"], validators=[validators.validate_birthday],
                                       format="%d.%m.%Y")
    relatives = MySlugRelatedField(many=True, slug_field='citizen_id')

    class Meta:
        model = Citizen
        fields = ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']
        read_only_fields = ['citizen_id']
