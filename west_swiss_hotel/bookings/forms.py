from django import forms
from .models import Room

class AvailabilityForm(forms.Form):
    room_type = forms.ChoiceField(choices=[('ALL', 'All Rooms')] + Room.RoomType.choices, required=False)
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    guests = forms.IntegerField(min_value=1, initial=1)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError("Check-out date must be after check-in date.")
        return cleaned_data

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-hotel-neutral-50 rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'Your Full Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-hotel-neutral-50 rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'your.email@example.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-hotel-neutral-50 rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': '+234 XXX XXX XXXX'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-hotel-neutral-50 rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-hotel-neutral-50 rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'Your message...',
            'rows': 5
        })
    )

class BookingForm(forms.Form):
    guest_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'Full Name'
        })
    )
    guest_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'email@example.com'
        })
    )
    guest_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': '+234 XXX XXX XXXX'
        })
    )
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all'
        })
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all'
        })
    )
    number_of_guests = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all'
        })
    )
    special_requests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-hotel-neutral-200 bg-white rounded-lg p-3 text-sm focus:ring-2 focus:ring-hotel-teal outline-none transition-all',
            'placeholder': 'Any special requests? (Optional)',
            'rows': 3
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError("Check-out date must be after check-in date.")
            
            # Check if dates are in the past
            from datetime import date
            if check_in < date.today():
                raise forms.ValidationError("Check-in date cannot be in the past.")
        
        return cleaned_data

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'total_inventory', 'price_per_night', 'view_type', 'description', 'image', 'has_wifi', 'has_breakfast', 'has_ac']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'w-full border border-slate-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-hotel-teal/20 outline-none'}),
            'total_inventory': forms.NumberInput(attrs={'class': 'w-full border border-slate-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-hotel-teal/20 outline-none', 'min': 1}),
            'price_per_night': forms.NumberInput(attrs={'class': 'w-full border border-slate-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-hotel-teal/20 outline-none'}),
            'view_type': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-hotel-teal/20 outline-none', 'placeholder': 'e.g. Garden View'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-slate-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-hotel-teal/20 outline-none', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'w-full border border-slate-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-hotel-teal/20 outline-none'}),
        }
