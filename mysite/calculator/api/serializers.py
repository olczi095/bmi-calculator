from rest_framework import serializers

from calculator.models import Person


class PersonSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(source='id')
    user_id = serializers.IntegerField(source='user.id', required=False)

    class Meta:
        model = Person
        fields = ('name',  'person_id', 'user_id', 'weight',
                  'height', 'gender', 'age', 'pal')
