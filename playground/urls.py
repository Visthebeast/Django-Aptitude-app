from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home,name="home"),
    path('api/get-mcq/',views.get_mcq, name="get_mcq"),
    path('mcq/',views.mcq,name="mcq"),
    path('submit-mcq/', views.submit_mcq, name="submit_mcq"),
    path('update_timer/', views.update_timer, name='update_timer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
]

