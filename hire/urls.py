from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('profile', views.profile),
    path('logout',views.logout),
    path('new',views.new),
    path('create',views.create),
    path('con', views.con),
    path('<int:con_id>/edit', views.edit),
    path('<int:con_id>/update', views.update),
    path('<int:con_id>/remove', views.remove),
    path('<int:con_id>', views.con),
]