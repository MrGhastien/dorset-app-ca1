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
    path('users/<str:userNickname>/keys', views.userKeysView, name='user-keys'),
    path('users/<str:userNickname>', views.userDetailView, name='user-detail'),
    path('users/<str:userNickname>/send', views.updateUser, name='user-update'),
    path('users/<str:userNickname>/delete', views.userDeleteView, name='user-delete'),
    path('users/<str:userNickname>/delete/send', views.deleteUser, name='user-delete-do'),
    path('new-user', views.userAddView, name='user-new'),
    path('new-user/send', views.addUser, name='user-add'),

    path('users/<str:userNickname>/new-key', views.keyAddView, name='add-key'),
    path('users/<str:userNickname>/new-key/send', views.addKey, name='key-send'),
    path('keys/<int:keyId>', views.keyDetailView, name='key-detail'),
    path('keys/<int:keyId>/send', views.updateKey, name='key-update'),
    path('keys/<int:keyId>/delete', views.keyDeleteView, name='key-delete'),
    path('keys/<int:keyId>/delete/send', views.deleteKey, name='key-delete-do'),
]