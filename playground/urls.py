from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('api/get-mcq/',views.get_mcq, name="get_mcq"),
    path('mcq/',views.mcq,name="mcq")
]

