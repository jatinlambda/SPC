# from django.conf.urls import url, include
# from rest_framework import routers
# from rest_framework.urlpatterns import format_suffix_patterns
# from api import views
#
# router = routers.DefaultRouter()
# # router.register(r'users', views.UserViewSet)
# # router.register(r'groups', views.GroupViewSet)
# #router.register(r'', views.FileViewSet)
# router.register(r'file/', views.FileList.as_view(),basename='file-list')
#
#
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

from django.urls import path
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path(r'filelist/', views.FileList.as_view()),
    path(r'fileupload/', views.FileUpload.as_view()),
    re_path(r'^filedownload/(?P<path>.+)/', views.FileDownload.as_view()),
    re_path(r'^fileupdate/(?P<path>.+)/', views.FileUpdate.as_view()),
    # path(r'filedownload/()', views.FileDownload.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
