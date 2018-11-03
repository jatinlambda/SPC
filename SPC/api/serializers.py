from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import ModelField
from user.models import File


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')
class CoordinateField(serializers.Field):
    #
    def to_representation(self, value):
        ret = {
            "docfile": value.docfile,
            # "y": value.y_coordinate
        }
        return value.docfile

    def to_internal_value(self, data):
        ret = {
        'docfile': data.encode('utf-8'),
        }
        return ret

class FileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # genre = serializers.SerializerMethodField()
    docfile = CoordinateField(source='*')
    # docfile = CoordinateField()
    # docfile = ModelField(model_field=File.get_field('docfile'))
    # docfile = serializers.JSONField()

    def get_genre(self, instance):
        # get the language id from the view kwargs
        language_id = self.context['view'].kwargs['language_pk']
        # get the genre
        try:
            docfile = instance.docfile#GenresVideo.objects.get(genre_id=instance.genre_id, language_id=language_id).name
        except GenresVideo.DoesNotExist:
            genre_name = None
        # return the formatted output
        return genre_name

    class Meta:
        model = File
        fields = ('owner', 'path', 'sha256', 'docfile')


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')
