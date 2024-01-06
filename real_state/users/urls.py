from django.urls import path
from users import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
]
