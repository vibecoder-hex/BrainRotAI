from django.urls import path
from brainrotapp import views

app_name = "brainrotapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('about_user/', views.about_user, name="about_user")
]