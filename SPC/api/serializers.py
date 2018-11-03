from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import ModelField
from user.models import File


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class FileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # docfile = ModelField(model_field=File.get_field('docfile'))
    # docfile = serializers.JSONField()
    class Meta:
        model = File
        fields = ('owner', 'path', 'sha256', 'docfile')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
