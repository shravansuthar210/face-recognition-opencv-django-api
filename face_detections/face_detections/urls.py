
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('face.urls')),
    path('', views.hy),
    url('facedetection',views.facedetecions),
    url("faceadd",views.add_face),
    url("faceidentify",views.face_name),
]
# urlpatterns = [
#     path('', views.hy),
#     url('facedetection',views.facedetecions),
#     url("faceadd",views.add_face),
#     url("faceidentify",views.face_name),
# ]
