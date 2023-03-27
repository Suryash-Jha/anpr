from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


# Create your views here.

urlpatterns = [
    path('', views.tempResult),
    path('temp/', views.home),
    path('getRecvdImg/<int:currTime>', views.getRecvdImg),
    path('getClearImg/<int:currTime>', views.getClearImg),
    path('getExtractedImg/<int:currTime>', views.getExtractedImg),
    path('apiExtractedData/<int:currTime>', views.apiExtractedData),
    path('ocr/', views.storeData),


    # path('profile/', views.profile),
]
