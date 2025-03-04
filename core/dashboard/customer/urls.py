from django.urls import path
from . import views

app_name = "dash_customer"
urlpatterns = [
    path("home/", views.CustomerDashboardHomeView.as_view(), name="home")
]