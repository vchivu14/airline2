from django.urls import path
from . import views

app_name = 'flights'
urlpatterns = [
    path("", views.index, name="index"),
    path("addflight/", views.addflight, name="addflight"),
    path("<int:flight_id>/", views.flight, name="flight"),
    path("<int:flight_id>/book/", views.signup, name="book"),
    path("<int:flight_id>/signup/", views.signup, name="signup"),
]