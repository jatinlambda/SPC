import hashlib

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import ModelField
from user.models import File


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')
class DataField(serializers.Field):
    #
    def to_representation(self, value):
        return value.docfile

    def to_internal_value(self, data):
        ret = {
        'docfile': data.encode('utf-8'),
        }
        return ret

class ShaField(serializers.Field):

    def to_representation(self, value):
        return value.sha256

    def get_value(self, instance):
        return instance['docfile']

    def to_internal_value(self, data):
        sha = hashlib.sha256()
        sha.update(data.encode('utf-8'))
        sha256 = sha.hexdigest()
        ret = {
        'sha256': sha256,
        }
        return ret

class FileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    docfile = DataField(source='*')
    sha256 = ShaField(source='*')
    class Meta:
        model = File
        fields = ('owner', 'path', 'sha256', 'docfile')

class FileListSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    sha256 = ShaField(source='*')
    class Meta:
        model = File
        fields = ('path', 'sha256')
