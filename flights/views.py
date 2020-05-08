from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger, Airport
from django.db.models import F


def index(request):
    context = {
        "flights": Flight.objects.all(),
        "airports": Airport.objects.all(),
        "passengers": Passenger.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    # try:
    #     flight = Flight.objects.get(pk=flight_id)
    # except Flight.DoesNotExist:
    #     raise Http404("Flight does not exist")
    flight = get_object_or_404(Flight, pk=flight_id)
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    seats = Flight.objects.get(pk=flight_id).seats
    if seats >= 1:
        try:
            passenger_id = int(request.POST["passenger"])
            flight = Flight.objects.get(pk=flight_id)
            passenger = Passenger.objects.get(pk=passenger_id)
        except KeyError:
            return render(request, "flights/error.html", {"message": "No selection."})
        except Flight.DoesNotExist:
            return render(request, "flights/error.html", {"message": "No Flight."})
        except Passenger.DoesNotExist:
            return render(request, "flights/error.html", {"message": "No passenger."})
        passenger.flights.add(flight)
        flight.seats = F('seats') - 1
        flight.save()
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
    else:
        return HttpResponse("No seats available")
    
def deletebooking(request, flight_id):
    seats = Flight.objects.get(pk=flight_id).seats
    passengers = Flight.objects.get(pk=flight_id).passengers.all()
    if passengers:
        try:
            passenger_id = int(request.POST["passenger"])
            flight = Flight.objects.get(pk=flight_id)
            passenger = Passenger.objects.get(pk=passenger_id)
        except KeyError:
            return render(request, "flights/error.html", {"message": "No selection."})
        except Flight.DoesNotExist:
            return render(request, "flights/error.html", {"message": "No Flight."})
        except Passenger.DoesNotExist:
            return render(request, "flights/error.html", {"message": "No passenger."})
        passenger.flights.remove(flight)
        flight.seats = F('seats') + 1
        flight.save()
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
    else:
        return HttpResponse("Plane is empty")
    
def signup(request, flight_id):
    seats = Flight.objects.get(pk=flight_id).seats
    if seats > 1:
        try:
            first_name = request.POST["first"]
            last_name = request.POST["last"]
            flight = Flight.objects.get(pk=flight_id)
        except KeyError:
            return render(request, "flights/error.html", {"message": "No entries."})
        passenger = Passenger(first=first_name, last=last_name)
        passenger.save()
        passenger.flights.add(flight)
        flight.seats = F('seats') - 1
        flight.save()
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
    else:
        return HttpResponse("No seats available")
    
def addflight(request):
    try:
        origin = request.POST["airport1"]
        a_origin = Airport.objects.get(pk=origin)
        destination = request.POST["airport2"]
        a_destination = Airport.objects.get(pk=destination)
        duration = request.POST["duration"]
        seats = request.POST["seats"]
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection."})
    flight = Flight(origin=a_origin, destination=a_destination, duration=duration, seats=seats)
    flight.save()
    return HttpResponseRedirect(reverse("flights:index"))

def addairport(request):
    try:
        name = request.POST["city"]
        code = request.POST["code"]
    except KeyError:
        return render(request, "flights/error.html", {"message": "No entries."})
    airport = Airport(city=name, code=code)
    airport.save()
    return HttpResponseRedirect(reverse("flights:index"))

def addpassenger(request):
    try:
        first = request.POST["first"]
        last = request.POST["last"]
    except KeyError:
        return render(request, "flights/error.html", {"message": "No entries."})
    passenger = Passenger(first=first, last=last)
    passenger.save()
    return HttpResponseRedirect(reverse("flights:index"))

def deletepassenger(request):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No entries."})
    passenger.delete()
    return HttpResponseRedirect(reverse("flights:index"))
