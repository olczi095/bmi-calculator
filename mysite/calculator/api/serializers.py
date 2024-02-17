from rest_framework import serializers

from calculator.models import CalculatedData, Person


class PersonSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(source='id', read_only=True)
    user_id = serializers.IntegerField(source='user.id', required=False, read_only=True)

    class Meta:
        model = Person
        fields = ('name',  'person_id', 'user_id', 'weight',
                  'height', 'gender', 'age', 'pal')


class CalculatedDataSerializer(serializers.ModelSerializer):
    calculateddata_id = serializers.IntegerField(source='id', read_only=True)
    person_name = serializers.CharField(source='person.name', read_only=True)
    person_id = serializers.IntegerField(source='person.id', read_only=True)
    user_id = serializers.IntegerField(
        source='person.user.id', required=False, read_only=True)

    class Meta:
        model = CalculatedData
        fields = ('calculateddata_id', 'person_name', 'person_id', 'user_id',
                  'bmi', 'bmi_category', 'bmr', 'pal', 'tmr')
