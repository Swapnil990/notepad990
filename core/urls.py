from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login_custom,name='login'),
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('token_send',views.token_send,name='token_send'),
    path('error',views.error,name='error'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('create',views.create,name='create'),
    path('addnote',views.addnote,name='addnote'),
    path('update/<int:id>',views.update,name='update'),
    path('update/save/<int:id>',views.save_update,name='save'),
    path('delete/<int:id>',views.delete_note,name='delete'),
    path('logout',views.logout_custom,name='logout'),
]
