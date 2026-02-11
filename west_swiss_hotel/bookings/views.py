from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Booking, OTARate, ContactMessage
from .forms import AvailabilityForm, ContactForm, BookingForm, RoomForm

@login_required(login_url='admin_login')
def add_room(request):
    if not request.user.is_staff: return redirect('home')
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New room added successfully!')
            return redirect('admin_rooms')
    else:
        form = RoomForm()
    
    message_count = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'bookings/admin/add_room.html', {'form': form, 'message_count': message_count})
from datetime import datetime, date, timedelta

def check_availability(request):
    """Handle availability search and results"""
    ota_rates = OTARate.objects.all()
    form_submitted = False
    
    # Official direct starting price
    official_rate_obj = Room.objects.order_by('price_per_night').first()
    official_price = official_rate_obj.price_per_night if official_rate_obj else 80500

    # Enrich OTA rates
    updated_ota_rates = []
    for rate in ota_rates:
        rate.price_diff = rate.price - official_price
        updated_ota_rates.append(rate)

    rooms_with_status = []
    
    if request.GET.get('check_in') or request.GET.get('check_out'):
        form_submitted = True
        form = AvailabilityForm(request.GET)
        
        if form.is_valid():
            cd = form.cleaned_data
            check_in = cd['check_in']
            check_out = cd['check_out']
            room_type_filter = cd.get('room_type', 'ALL')

            # Fetch all room categories
            rooms = Room.objects.all()
            if room_type_filter and room_type_filter != 'ALL':
                rooms = rooms.filter(room_type=room_type_filter)

            for room in rooms:
                available_count = room.get_available_inventory(check_in, check_out)
                rooms_with_status.append({
                    'room': room,
                    'available_count': available_count,
                    'is_available': available_count > 0
                })
        else:
            form = AvailabilityForm(request.GET)
    else:
        form = AvailabilityForm()
        # Default display when no search
        for room in Room.objects.all():
            rooms_with_status.append({
                'room': room,
                'available_count': room.total_inventory,
                'is_available': True
            })

    context = {
        'form': form,
        'rooms_with_status': rooms_with_status,
        'ota_rates': updated_ota_rates,
        'official_price': official_price,
        'form_submitted': form_submitted,
    }
    return render(request, 'bookings/availability_results.html', context)

def home_view(request):
    """Hotel homepage with default today's availability"""
    ota_rates = OTARate.objects.all()
    rooms = Room.objects.all().order_by('price_per_night')
    
    # Check availability for today to tomorrow
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    rooms_with_status = []
    for room in rooms:
        available_count = room.get_available_inventory(today, tomorrow)
        rooms_with_status.append({
            'room': room,
            'available_count': available_count,
            'is_available': available_count > 0
        })

    # Official starting price
    cheapest_room = rooms.first()
    official_price = cheapest_room.price_per_night if cheapest_room else 80500

    updated_ota_rates = []
    for rate in ota_rates:
        rate.price_diff = rate.price - official_price
        updated_ota_rates.append(rate)

    context = {
        'ota_rates': updated_ota_rates,
        'official_price': official_price,
        'rooms_with_status': rooms_with_status,
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
            
            # Save to Database
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
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
                
                success_msg = 'Thank you for contacting us! We will get back to you shortly.'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'status': 'success', 'message': success_msg})
                    
                messages.success(request, success_msg)
                return redirect('/#contact')
            except Exception as e:
                error_msg = 'There was an error sending your message. Please try again or contact us directly.'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=500)
                messages.error(request, error_msg)
        else:
            error_msg = 'Please correct the errors in the form.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
                return JsonResponse({'status': 'error', 'message': error_msg, 'errors': form.errors}, status=400)
            messages.error(request, error_msg)
    else:
        form = ContactForm()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
        
    return redirect('/#contact')

def book_room(request, room_id):
    """Handle room booking form display and submission"""
    try:
        room = Room.objects.get(id=room_id)
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
            
            # Check for conflicting bookings (Inventory check)
            conflicting_bookings_count = Booking.objects.filter(
                room=room,
                status__in=['PENDING', 'CONFIRMED', 'CHECKED_IN'],
                check_in__lt=check_out,
                check_out__gt=check_in
            ).count()
            
            if conflicting_bookings_count >= room.total_inventory:
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
            
            # Send confirmation email
            try:
                send_mail(
                    f'Booking Confirmation - {room.get_room_type_display()}',
                    f"""Dear {booking.guest_name},

Thank you for your booking at West-Swiss Hotel Aba!

Booking Details:
- Reference: #{booking.display_id}
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
                pass
            
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        initial_data = {'number_of_guests': guests_default}
        if check_in_default:
            try:
                initial_data['check_in'] = datetime.strptime(check_in_default, '%Y-%m-%d').date()
            except: pass
        if check_out_default:
            try:
                initial_data['check_out'] = datetime.strptime(check_out_default, '%Y-%m-%d').date()
            except: pass
        
        form = BookingForm(initial=initial_data)
    
    context = {'room': room, 'form': form, 'check_in': check_in_default, 'check_out': check_out_default}
    return render(request, 'bookings/book_room.html', context)

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking.objects.select_related('room'), id=booking_id)
    num_nights = (booking.check_out - booking.check_in).days
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking, 'num_nights': num_nights})

def room_detail(request, room_id):
    """Display detailed information about a specific room"""
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'bookings/room_detail.html', {'room': room})

# --- Admin Custom Views ---

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or access denied.')
            
    return render(request, 'bookings/admin/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
        
    bookings = Booking.objects.select_related('room').all().order_by('-created_at')
    rooms = Room.objects.all()
    ota_rates = OTARate.objects.all()
    contact_messages = ContactMessage.objects.all()
    
    # Stats
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='PENDING').count()
    today_bookings = bookings.filter(created_at__date=date.today()).count()
    total_rooms = rooms.count()
    available_rooms_count = len([r for r in rooms if r.is_available(date.today(), date.today() + timedelta(days=1))])
    message_count = contact_messages.filter(is_read=False).count()
    
    # Revenue (last 30 days)
    last_30_days = date.today() - timedelta(days=30)
    monthly_revenue = bookings.filter(created_at__date__gte=last_30_days, status__in=['CONFIRMED', 'CHECKED_IN', 'COMPLETED']).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    context = {
        'bookings': bookings[:10], # Latest 10
        'all_bookings_count': total_bookings,
        'pending_bookings_count': pending_bookings,
        'today_bookings_count': today_bookings,
        'total_rooms_count': total_rooms,
        'available_rooms_count': available_rooms_count,
        'monthly_revenue': monthly_revenue,
        'rooms': rooms,
        'ota_rates': ota_rates,
        'message_count': message_count,
    }

    return render(request, 'bookings/admin/dashboard.html', context)

@login_required(login_url='admin_login')
def admin_bookings(request):
    if not request.user.is_staff: return redirect('home')
    bookings = Booking.objects.select_related('room').all().order_by('-created_at')
    message_count = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'bookings/admin/bookings.html', {'bookings': bookings, 'message_count': message_count})

@login_required(login_url='admin_login')
def admin_rooms(request):
    if not request.user.is_staff: return redirect('home')
    rooms = Room.objects.all().order_by('room_type')
    message_count = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'bookings/admin/rooms.html', {'rooms': rooms, 'message_count': message_count})

@login_required(login_url='admin_login')
def admin_messages(request):
    if not request.user.is_staff: return redirect('home')
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    # Mark all as read when visiting messages page
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    message_count = 0
    return render(request, 'bookings/admin/messages.html', {'contact_messages': contact_messages, 'message_count': message_count})

@login_required(login_url='admin_login')
def delete_message(request, message_id):
    if not request.user.is_staff: return redirect('home')
    if request.method == 'POST':
        message = get_object_or_404(ContactMessage, id=message_id)
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    return redirect('admin_messages')

@login_required(login_url='admin_login')
def update_booking_status(request, booking_id):
    if not request.user.is_staff: return redirect('home')
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in [s[0] for s in Booking.Status.choices]:
            booking.status = status
            booking.save()
            messages.success(request, f'Booking #{booking.display_id} status updated to {status}.')
    return redirect('admin_bookings')

@login_required(login_url='admin_login')
def admin_revenue(request):
    """View detailed revenue statistics"""
    if not request.user.is_staff: return redirect('home')
    
    # Base query: confirmed bookings
    paid_bookings = Booking.objects.filter(status__in=['CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT'])
    
    # Totals
    total_revenue = paid_bookings.aggregate(total=Sum('total_price'))['total'] or 0
    
    # Monthly
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    monthly_revenue = paid_bookings.filter(created_at__gte=start_of_month).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Last 30 Days
    last_30 = today - timedelta(days=30)
    last_30_days_revenue = paid_bookings.filter(created_at__gte=last_30).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Pending (Potential)
    pending_revenue = Booking.objects.filter(status='PENDING').aggregate(total=Sum('total_price'))['total'] or 0
    
    # Revenue by Room Type
    revenue_by_type = paid_bookings.values('room__room_type').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('-total')
    
    # Calculate percentages and labels
    room_type_labels = dict(Room.RoomType.choices)
    for item in revenue_by_type:
        item['percentage'] = (item['total'] / total_revenue * 100) if total_revenue > 0 else 0
        item['label'] = room_type_labels.get(item['room__room_type'], item['room__room_type'])
    
    recent_transactions = Booking.objects.all().order_by('-created_at')[:10]
    message_count = ContactMessage.objects.filter(is_read=False).count()
    
    context = {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'last_30_days_revenue': last_30_days_revenue,
        'pending_revenue': pending_revenue,
        'revenue_by_type': revenue_by_type,
        'recent_transactions': recent_transactions,
        'message_count': message_count
    }
    return render(request, 'bookings/admin/revenue.html', context)

@login_required(login_url='admin_login')
def edit_room(request, room_id):
    """Edit an existing room"""
    if not request.user.is_staff: return redirect('home')
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'{room.get_room_type_display()} updated successfully!')
            return redirect('admin_rooms')
    else:
        form = RoomForm(instance=room)
        
    message_count = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'bookings/admin/edit_room.html', {'form': form, 'room': room, 'message_count': message_count})
