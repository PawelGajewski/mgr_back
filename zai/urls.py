from django.urls import path, include
from . import views
from znaki.znaki import urls

urlpatterns = [
    path(r'^api_auth/', include('rest_framework.urls')),
    path('', views.index, name='index'),
    path('api/', include(urls))
]