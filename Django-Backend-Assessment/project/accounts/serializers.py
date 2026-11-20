from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # TODO: Candidate implementation
        # Configure field validation, normalize input, and report duplicate values.
        raise NotImplementedError

    def create(self, validated_data):
        # TODO: Candidate implementation
        # Hash the password, save the account, and handle database uniqueness errors.
        raise NotImplementedError
