from django.http import HttpResponse
from user.models import File
from .serializers import FileSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class FileList(APIView):

    def get(self, request, format=None):
        # permission_classes = (permissions.IsAuthenticated,)

        if request.user.is_authenticated :
                queryset = File.objects.filter(owner=self.request.user)
        else:
            queryset = None
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializer = FileSerializer(data=request.data)
            # print(request.data['owner'])
            # print(request.user.id)
            if request.user.id == request.data['owner'] :
                if serializer.is_valid() :
                #if serializer.data['owner'] == request.user :
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else :
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else :
            return HttpResponse('Unauthorized', status=401)









# from django.contrib.auth.models import User, Group
# from rest_framework import viewsets
# from api.serializers import FileSerializer, UserSerializer, GroupSerializer
# from user.models import File
# from rest_framework import permissions
#
# class FileViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = File.objects.all()  # .order_by('-date_joined')
#     serializer_class = FileSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     def get_queryset(self):
#         if self.request.user.is_authenticated :
#             if self.action == 'list':
#                 return self.queryset.filter(owner=self.request.user)
#             return self.queryset
#         else :
#             return None
#
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
