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


class BMRSerializer(serializers.Serializer):
    age = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=['male', 'female'])
    height = serializers.FloatField()
    weight = serializers.FloatField()

    def validate_age(self, value):
        """
        Validate that the age is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Age must be a positive integer")
        return value

    def validate_height(self, value):
        """
        Validate that the height is an positive integer, less than 300.
        """
        if value <= 0:
            raise serializers.ValidationError("Height must be greater than 0")
        elif value >= 300:
            raise serializers.ValidationError("Height must be less than 300")
        else:
            return value

    def validate_weight(self, value):
        """
        Validate that the weight is a positive integer, less than 1000.
        """
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        elif value >= 1000:
            raise serializers.ValidationError("Weight must be less than 1000")
        else:
            return value
