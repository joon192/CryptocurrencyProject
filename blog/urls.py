from django.urls import path
from blog import views

app_name = "user"

urlpatterns = [
    path("", views.main, name="main"),
    path("detail", views.detail, name="detail"),
    path("recommend", views.recommend, name="recommend"),
    path("result", views.result, name="result"),
    path("about", views.about, name="about"),
    path("signup", views.signup, name="signup"),
]