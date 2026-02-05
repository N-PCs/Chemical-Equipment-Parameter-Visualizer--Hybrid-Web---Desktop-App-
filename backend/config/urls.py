"""
URL Configuration for ChemEquip Visualizer Backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "message": "ChemEquip Visualizer Backend API",
        "api_root": "/api/",
        "docs": "https://github.com/vandan-02/Chemical-Equipment-Parameter-Visualizer--Hybrid-Web---Desktop-App-"
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('equipment.urls')),
]
