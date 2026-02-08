from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Room, Booking, OTARate
from .forms import AvailabilityForm, ContactForm, BookingForm
from datetime import datetime, date

def check_availability(request):
    # Default: show all available rooms if no search is performed
    available_rooms = Room.objects.filter(is_available=True)
    ota_rates = OTARate.objects.all()
    form_submitted = False
    
    # Official direct starting price (usually the cheapest room)
    official_rate_obj = Room.objects.order_by('price_per_night').first()
    official_price = official_rate_obj.price_per_night if official_rate_obj else 80500

    # Enrich OTA rates with price difference
    updated_ota_rates = []
    for rate in ota_rates:
        rate.price_diff = rate.price - official_price
        updated_ota_rates.append(rate)

    # Check if GET parameters exist (form was submitted)
    if request.GET.get('check_in') or request.GET.get('check_out'):
        form_submitted = True
        form = AvailabilityForm(request.GET)
        
        if form.is_valid():
            cd = form.cleaned_data
            check_in = cd['check_in']
            check_out = cd['check_out']
            room_type = cd.get('room_type', 'ALL')

            # Find overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            
            booked_room_ids = overlapping_bookings.values_list('room_id', flat=True)
            rooms_query = Room.objects.filter(is_available=True).exclude(id__in=booked_room_ids)
            
            if room_type and room_type != 'ALL':
                rooms_query = rooms_query.filter(room_type=room_type)
                
            available_rooms = rooms_query
        else:
            # Form has errors, show all rooms but preserve form for error display
            available_rooms = Room.objects.filter(is_available=True)
    else:
        # No search performed, create empty form
        form = AvailabilityForm()

    context = {
        'form': form,
        'available_rooms': available_rooms,
        'ota_rates': updated_ota_rates,
        'official_price': official_price,
        'form_submitted': form_submitted,
    }
    return render(request, 'bookings/availability_results.html', context)

def home_view(request):
    ota_rates = OTARate.objects.all()
    official_price = 80500
    rooms = Room.objects.all()
    
    # Get the cheapest room price for the direct rate display
    cheapest_room = Room.objects.order_by('price_per_night').first()
    if cheapest_room:
        official_price = cheapest_room.price_per_night

    # Enrich OTA rates with price difference
    updated_ota_rates = []
    for rate in ota_rates:
        rate.price_diff = rate.price - official_price
        updated_ota_rates.append(rate)

    context = {
        'ota_rates': updated_ota_rates,
        'official_price': official_price,
        'rooms': rooms,
    }
    return render(request, 'bookings/index.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            email = cd['email']
            phone = cd.get('phone', 'Not provided')
            subject = cd['subject']
            message = cd['message']
            
            # Prepare email content
            email_subject = f"Contact Form: {subject}"
            email_message = f"""
New contact form submission from West-Swiss Hotel website:

Name: {name}
Email: {email}
Phone: {phone}

Subject: {subject}

Message:
{message}
"""
            
            try:
                # Send email to hotel
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  # Hotel's email
                    fail_silently=False,
                )
                
                messages.success(request, 'Thank you for contacting us! We will get back to you shortly.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again or contact us directly.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ContactForm()
    
    return redirect('home')

def book_room(request, room_id):
    """Handle room booking form display and submission"""
    try:
        room = Room.objects.get(id=room_id, is_available=True)
    except Room.DoesNotExist:
        messages.error(request, 'Sorry, this room is not available.')
        return redirect('check_availability')
    
    # Get pre-filled dates from query params if coming from availability search
    check_in_default = request.GET.get('check_in', '')
    check_out_default = request.GET.get('check_out', '')
    guests_default = request.GET.get('guests', 2)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            check_in = cd['check_in']
            check_out = cd['check_out']
            
            # Check for conflicting bookings
            conflicting_bookings = Booking.objects.filter(
                room=room,
                status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            
            if conflicting_bookings.exists():
                messages.error(request, 'Sorry, this room is no longer available for the selected dates.')
                return redirect('check_availability')
            
            # Calculate total price
            num_nights = (check_out - check_in).days
            total_price = room.price_per_night * num_nights
            
            # Create booking
            booking = Booking.objects.create(
                room=room,
                guest_name=cd['guest_name'],
                guest_email=cd['guest_email'],
                guest_phone=cd['guest_phone'],
                check_in=check_in,
                check_out=check_out,
                number_of_guests=cd['number_of_guests'],
                special_requests=cd.get('special_requests', ''),
                total_price=total_price,
                status='PENDING'
            )
            
            # Send confirmation email (console backend for now)
            try:
                send_mail(
                    f'Booking Confirmation - {room.get_room_type_display()}',
                    f"""Dear {booking.guest_name},

Thank you for your booking at West-Swiss Hotel Aba!

Booking Details:
- Room: {room.get_room_type_display()}
- Check-in: {booking.check_in.strftime('%B %d, %Y')}
- Check-out: {booking.check_out.strftime('%B %d, %Y')}
- Guests: {booking.number_of_guests}
- Total: ₦{booking.total_price:,.0f}

We look forward to welcoming you!

Best regards,
West-Swiss Hotel Aba
""",
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.guest_email],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Don't fail booking if email fails
            
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        # Pre-fill form with availability search data
        initial_data = {
            'number_of_guests': guests_default
        }
        if check_in_default:
            try:
                initial_data['check_in'] = datetime.strptime(check_in_default, '%Y-%m-%d').date()
            except:
                pass
        if check_out_default:
            try:
                initial_data['check_out'] = datetime.strptime(check_out_default, '%Y-%m-%d').date()
            except:
                pass
        
        form = BookingForm(initial=initial_data)
    
    context = {
        'room': room,
        'form': form,
        'check_in': check_in_default,
        'check_out': check_out_default,
    }
    return render(request, 'bookings/book_room.html', context)

def booking_confirmation(request, booking_id):
    """Display booking confirmation"""
    try:
        booking = Booking.objects.select_related('room').get(id=booking_id)
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found.')
        return redirect('home')
    
    num_nights = (booking.check_out - booking.check_in).days
    
    context = {
        'booking': booking,
        'num_nights': num_nights,
    }
    return render(request, 'bookings/booking_confirmation.html', context)
