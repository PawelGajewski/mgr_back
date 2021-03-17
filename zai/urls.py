from django.urls import path, include
from . import views
from znaki.znaki import urls

urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', include(urls))
]