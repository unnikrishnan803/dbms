from django import forms
from django.core.validators import RegexValidator
from .models import User, BloodRequest, BloodDonation, BloodInventory, EmergencyContact


class UserForm(forms.ModelForm):
    # Enhanced phone validation for Indian numbers
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-input',
            'placeholder': 'Enter your phone number',
            'title': 'Enter your phone number'
        })
    )
    
    class Meta:
        model = User
        fields = ['name', 'age', 'gender', 'email', 'phone', 'city', 'district', 'taluk', 'blood_group', 'photo', 'willing_to_donate']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your full name',
                'autocomplete': 'name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'min': '18',
                'max': '100',
                'placeholder': 'Age (18-100)'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'your.email@example.com',
                'autocomplete': 'email'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your city name',
                'autocomplete': 'address-level2'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'id': 'district-select'
            }),
            'taluk': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'id': 'taluk-select'
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*',
                'data-preview': 'photo-preview'
            }),
            'willing_to_donate': forms.CheckboxInput(attrs={
                'class': 'form-check-input form-check-input-lg'
            }),
        }


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'hospital_name', 'required_date']
        widgets = {
            'blood_group': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'placeholder': 'Select blood group'
            }),
            'hospital_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter hospital name'
            }),
            'required_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date',
                'min': 'today'
            }),
        }


class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = BloodDonation
        fields = ['donor', 'donation_date', 'hospital_name', 'blood_group', 'units_donated', 'notes']
        widgets = {
            'donor': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'donation_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date'
            }),
            'hospital_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter hospital name'
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'units_donated': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'min': '1',
                'max': '5',
                'placeholder': '1-5 units'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': '4',
                'placeholder': 'Additional notes about the donation...'
            }),
        }


class BloodInventoryForm(forms.ModelForm):
    class Meta:
        model = BloodInventory
        fields = ['blood_group', 'available_units', 'critical_level']
        widgets = {
            'blood_group': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'available_units': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'min': '0',
                'placeholder': 'Available units'
            }),
            'critical_level': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'min': '1',
                'placeholder': 'Critical level threshold'
            }),
        }


class EmergencyContactForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$',
                message='Please enter a valid Indian phone number'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg phone-input',
            'placeholder': '+91 98765 43210'
        })
    )
    
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Contact person name'
            }),
            'relationship': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'e.g., Spouse, Parent, Sibling'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email (optional)'
            }),
        }


class BloodSearchForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'Any Blood Group')] + User.BLOOD_GROUP_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'id': 'search-blood-group'
        })
    )
    district = forms.ChoiceField(
        choices=[('', 'Any District')] + User.DISTRICT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'id': 'search-district-select'
        })
    )
    taluk = forms.ChoiceField(
        choices=[('', 'Any Taluk')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg',
            'id': 'search-taluk-select'
        })
    )
    min_age = forms.IntegerField(
        required=False,
        min_value=18,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Min Age (18+)'
        })
    )
    max_age = forms.IntegerField(
        required=False,
        min_value=18,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Max Age (100)'
        })
    )


