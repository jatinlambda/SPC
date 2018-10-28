from django.contrib.auth.models import User, Group
from rest_framework import serializers
from user.models import File


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.HyperlinkedIdentityField(
    #     view_name='user',
    #     #lookup_field='username'
    # )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class FileSerializer(serializers.ModelSerializer):
    # owner = serializers.HyperlinkedRelatedField(
    #     view_name='user',
    #     #lookup_field='username',
    #     many=False,
    #     read_only=True
    # )

    class Meta:
        model = File
        fields = ('owner', 'path', 'sha256', 'docfile')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
