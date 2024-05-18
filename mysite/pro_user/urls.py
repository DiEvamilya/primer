from django.urls import path
from . import views


app_name = "pro_user"

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]