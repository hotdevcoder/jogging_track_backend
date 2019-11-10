from rest_framework import serializers
from .models import Entry, User

class RoleValidatorMixin(object):
    def validate_role(self, value):
        # if 'django' not in value.lower():
        #     raise serializers.ValidationError("Blog post is not about Django")
        user = self.context['request'].user
        if user.is_manager and value in ['admin',]:
             raise serializers.ValidationError('User manager is not allowed to set admin role.')
        if user.is_user and value in ['admin', 'manager']:
             raise serializers.ValidationError('Regular user is allowed to change the role.')
        return value


class EntrySerializer(serializers.ModelSerializer):
  	class Meta:
  		model = Entry
  		fields = ['id', 'distance', 'duration', 'date']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'first_name', 'last_name', 'role']


class UserCreateSerializer(serializers.ModelSerializer, RoleValidatorMixin):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'password')
        read_only_fields = ('id', 'role')
        extra_kwargs = { 'password': { 'write_only': True } }

    def create(self, validated_data):

        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user