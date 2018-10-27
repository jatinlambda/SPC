from django.contrib.auth.models import User, Group
from rest_framework import serializers
from user.models import File


class FileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField()
    class Meta:
        model = File
        fields = ('owner', 'path', 'sha256', 'docfile')



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')