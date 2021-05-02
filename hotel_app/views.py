from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from django.contrib import messages
from .models import *
import datetime 

# Create your views here.
def hotel(request):
    hotels = Hotel.objects.all()
    context={
        'title':'Hotels',
        'hotels':hotels
    }
    return render(request, 'hotel_app/hotels.html', context)

@login_required
def booking(request, id):
    errors={}
    if request.method == "POST":
        customer = request.user
        hotel = Hotel.objects.get(id=id)
        no_of_rooms = request.POST.get('no_of_rooms')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        chkout=datetime.datetime.strptime(checkout_date,'%Y-%m-%d')
        now=datetime.datetime.now()
        chkin=datetime.datetime.strptime(checkin_date,'%Y-%m-%d')
        if chkin>chkout:
            errors['message']="Please enter valid dates."
            hotel = Hotel.objects.get(id=id)
            form = BookingForm() 
            booking_data = {'form':form, 'hotel':hotel,'errors':errors} 
            return render(request,'hotel_app/bookhotel_form.html',booking_data)
        elif now> chkin:
            errors['message']="Please enter valid dates2."
            hotel = Hotel.objects.get(id=id)
            form = BookingForm() 
            booking_data = {'form':form, 'hotel':hotel,'errors':errors} 
            return render(request,'hotel_app/bookhotel_form.html',booking_data)
        else:        
            Booking = BookHotel(customer=customer, 
                                hotel= hotel, 
                                no_of_rooms= no_of_rooms, 
                                checkin_date=checkin_date, 
                                checkout_date=checkout_date
                                # no_of_days=no_of_days
                            )
            Booking.save()
            messages.success(request, f'Booking Complete!!! Now Checkout for Payment!!!')

            return redirect('checkout')
    else:
        hotel = Hotel.objects.get(id=id)
        form = BookingForm() 
        booking_data = {'form':form, 'hotel':hotel} 
        return render(request, 'hotel_app/bookhotel_form.html', booking_data)


def checkout(request):
    item = BookHotel.objects.latest('id')
    context={'title':'BookHotel', 'item': item}
    return render(request, 'hotel_app/checkout.html', context)

def booking_details(request, id):
    items = BookHotel.objects.all().filter(customer_id=id)
    context={'title':'BookHotel', 'items': items}
    return render(request, 'hotel_app/booking_details.html', context)
