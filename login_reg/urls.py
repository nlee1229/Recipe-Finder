from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('reg_process', views.reg_process),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('delete/<id>', views.delete),
]