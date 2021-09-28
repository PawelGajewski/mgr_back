from django.contrib import admin
from django.urls import path, re_path
from .views import *
from rest_framework.authtoken import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', UserList.as_view()),
    path('signs', SignsList.as_view(), name="signs"),
    path('sign/<int:pk>', SignDetail.as_view()),
    path("signsymbol", SignSymbol.as_view(), name='symbol'),
    path('recognize', Recognize().as_view()),
    path('api-token-auth', views.obtain_auth_token, name='api-token-auth'),
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('auth', Auth.as_view()),
    path('logout', LogoutView.as_view()),
    path('recognitions', RecognitionList.as_view()),
    path('groups', RecognitioGroupList.as_view()),
]
