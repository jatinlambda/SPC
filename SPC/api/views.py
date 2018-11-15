from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from api.permissions import IsOwner
from user.models import File
from .serializers import FileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


# class FileList(APIView):
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get(self, request, format=None):
#         # permission_classes = (permissions.IsAuthenticated,)
#
#         if request.user.is_authenticated :
#                 queryset = File.objects.filter(owner=self.request.user)
#         else:
#             queryset = None
#         serializer = FileSerializer(queryset, many=True)
#         return Response(serializer.data)
#
# class FileDownload(APIView):
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get(self, request, path, format=None):
#         # permission_classes = (permissions.IsAuthenticated,)
#
#         if request.user.is_authenticated :
#             queryset = File.objects.filter(owner=self.request.user, path=path)
#             serializer = FileSerializer(queryset, many=True)
#             if serializer.data == []:
#                 return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(serializer.data[0])
#         else:
#             return HttpResponse('Unauthorized', status=401)
#
# class FileUpload(APIView):
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def post(self, request, format=None):
#         if request.user.is_authenticated:
#             serializer = FileSerializer(data=request.data)
#             # print(request.data['owner'])
#             # print(request.user.id)
#             if request.user.id == request.data['owner']:
#                 if serializer.is_valid() :
#                 #if serializer.data['owner'] == request.user :
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 HttpResponse(status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return HttpResponse('Unauthorized', status=401)
#
#
# class FileUpdate(APIView):
#     """
#     Retrieve, update or delete a file instance.
#     """
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get_object(self, request, path):
#         if request.user.is_authenticated:
#             try:
#                 return File.objects.get(owner=self.request.user, path=path)
#             except:
#                 raise Http404
#
#             # file = File.objects.get(owner=self.request.user, path=path)
#             # if not serializer.data:
#             #     return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
#             # else:
#             #     return Response(serializer.data[0])
#         else:
#             return HttpResponse('Unauthorized', status=401)
#
#     def get(self, request, path, format=None):
#         file = self.get_object(request, path)
#         serializer = FileSerializer(file)
#         return Response(serializer.data)
#
#     def put(self, request, path, format=None):
#         file = self.get_object(request, path)
#         #newfile = File(owner=file.owner, path=file.path, sha256=request.data['sha256'], docfile=request.data['docfile'])
#         serializer = FileSerializer(file, data=request.data)
#         if serializer.is_valid():
#             file.sha256 = request.data['sha256']
#             file.docfile = request.data['docfile']
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, path, format=None):
#         file = self.get_object(request, path)
#         file.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class FileViewSet(viewsets.ModelViewSet):
    lookup_field = 'path'
    lookup_value_regex = '.+'
    # parser_classes = (MultiPartParser, FormParser,)
    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)

    # queryset = File.objects.filter()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # serializer.save(=self.request.user)

    # def list(self, request, pk=None):
    #     if pk == None:
    #         supplements = models.Product.objects.filter(product_type=models.Product.SUPPLEMENT)
    #     else:
    #         supplements = models.Product.objects.get(product_type=models.Product.SUPPLEMENT, id=pk)
    #
    #     page = self.paginate_queryset(supplements)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(page, many=True)
    #     result_set = serializer.data
    #
    #     return Response(result_set)




