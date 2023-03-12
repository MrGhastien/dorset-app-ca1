from django.contrib import admin
from django.urls import path, include

from . import views


app_name = "sshkbase"
urlpatterns = [
    # Here we list urls that are valid.
    # Each url is tied to a function sending back a response for the browser,
    # containing the HTML and CSS files to display
    # The 'name' attribute is used in html files to get the associated url
    path('', views.indexView, name='index'),
    path('users', views.listView, name='list'),
    path('users/<str:userNickname>', views.userDetailView, name='user-detail'),
    path('update-user', views.userUpdateView, name='user-update'),
    path('update-user/send', views.updateUser, name='user-update-send'),
    path('delete-user', views.userDeleteView, name='user-delete'),
    path('delete-user/send', views.deleteUser, name='user-delete-send'),
    path('new-user', views.userAddView, name='user-new'),
    path('new-user/send', views.addUser, name='user-new-send'),
    path('login', views.userLoginView, name='user-login'),
    path('login/send', views.loginUser, name='user-login-send'),
    path('logout', views.logoutUser, name='user-logout'),

    path('new-key', views.keyAddView, name='add-key'),
    path('new-key/send', views.addKey, name='key-send'),
    path('keys', views.userKeysView, name='user-keys'),
    path('keys/<int:keyId>', views.keyDetailView, name='key-detail'),
    path('keys/<int:keyId>/send', views.updateKey, name='key-update'),
    path('keys/<int:keyId>/delete', views.keyDeleteView, name='key-delete'),
    path('keys/<int:keyId>/delete/send', views.deleteKey, name='key-delete-send'),
]