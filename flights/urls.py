from django.urls import path
from . import views

app_name = 'flights'
urlpatterns = [
    path("", views.index, name="index"),
    path("addairport/", views.addairport, name="addairport"),
    path("addflight/", views.addflight, name="addflight"),
    path("addpassenger/", views.addpassenger, name="addpassenger"),
    path("deletepassenger/", views.deletepassenger, name="deletepassenger"),
    path("<int:flight_id>/", views.flight, name="flight"),
    path("<int:flight_id>/book/", views.book, name="book"),
    path("<int:flight_id>/deletebooking/", views.deletebooking, name="deletebook"),
    path("<int:flight_id>/signup/", views.signup, name="signup"),
]