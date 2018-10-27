import base64

from django.contrib.auth.models import User
from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return 'documents/{0}/{1}'.format(str(instance.owner)+ "/" + str(instance.path), filename)


class FileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(owner=request.user)


class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # owner = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    sha256 = models.CharField(max_length=1000)
    docfile = models.BinaryField()

    objects = models.Manager()

    def __str__(self):
        return str(self.path)

    class Meta:
        unique_together = ("owner", "path")

    # docfile = models.FileField(upload_to=user_directory_path)
    #     db_column='docfile',
    #     null=True)
    # def set_data(self, data):
    #     self._data = base64.encodestring(data)
    #
    # def get_data(self):
    #     return base64.decodestring(self._docfile)
    #
    # docfile = property(get_data, set_data)

