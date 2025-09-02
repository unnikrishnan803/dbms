from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Q, Count
from .models import User, BloodRequest, BloodDonation, BloodInventory, EmergencyContact
from .forms import UserForm, BloodRequestForm, BloodDonationForm, BloodInventoryForm, EmergencyContactForm, BloodSearchForm


def home(request):
    # Get blood inventory status for dashboard
    inventory = BloodInventory.objects.all()
    critical_blood_groups = [inv for inv in inventory if inv.is_critical()]
    
    # Get recent donations
    recent_donations = BloodDonation.objects.select_related('donor').order_by('-donation_date')[:5]
    
    # Get statistics
    total_donors = User.objects.filter(willing_to_donate=True).count()
    total_donations = BloodDonation.objects.count()
    total_requests = BloodRequest.objects.count()
    
    return render(request, 'blood_app/home.html', {
        'inventory': inventory,
        'critical_blood_groups': critical_blood_groups,
        'recent_donations': recent_donations,
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_requests': total_requests,
        'districts': User.DISTRICT_CHOICES,
    })


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Registration successful!')
                return redirect('add_emergency_contacts', user_id=user.id)
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Registration error: {e}")
        else:
            print(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {errors[0]}')
    else:
        form = UserForm()
    return render(request, 'blood_app/register.html', {'form': form})


def donor_list(request):
    form = BloodSearchForm(request.GET)
    donors = User.objects.filter(willing_to_donate=True)
    
    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        district = form.cleaned_data.get('district')
        taluk = form.cleaned_data.get('taluk')
        min_age = form.cleaned_data.get('min_age')
        max_age = form.cleaned_data.get('max_age')
        
        if blood_group:
            donors = donors.filter(blood_group=blood_group)
        if district:
            donors = donors.filter(district=district)
        if taluk:
            donors = donors.filter(taluk=taluk)
        if min_age:
            donors = donors.filter(age__gte=min_age)
        if max_age:
            donors = donors.filter(age__lte=max_age)
    
    return render(request, 'blood_app/donor_list.html', {
        'donors': donors,
        'form': form,
        'blood_groups': User.BLOOD_GROUP_CHOICES,
        'districts': User.DISTRICT_CHOICES,
        'searched_at': timezone.now(),
    })


def request_blood(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = user
            blood_request.save()
            messages.success(request, 'Blood request submitted!')
            
            # Check inventory and notify if critical
            try:
                inventory = BloodInventory.objects.get(blood_group=blood_request.blood_group)
                if inventory.is_critical():
                    messages.warning(request, f'Warning: {blood_request.blood_group} blood is at critical level!')
            except BloodInventory.DoesNotExist:
                pass
            
            # Notify the requester (confirmation)
            try:
                if user.email:
                    send_mail(
                        subject=f"Your blood request for {blood_request.blood_group}",
                        message=(
                            f"Hi {user.name}, your request was received.\n\n"
                            f"Hospital: {blood_request.hospital_name}\n"
                            f"Required Date: {blood_request.required_date}\n"
                        ),
                        from_email=None,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
            except Exception:
                pass

            # Notify willing donors of the same blood group
            try:
                matching_donors = User.objects.filter(
                    willing_to_donate=True,
                    blood_group=blood_request.blood_group,
                ).exclude(email='')
                for donor in matching_donors:
                    send_mail(
                        subject=f"Urgent: {blood_request.blood_group} blood needed",
                        message=(
                            f"Dear {donor.name},\n\n"
                            f"A recipient has requested {blood_request.blood_group} blood.\n\n"
                            f"Requester: {user.name}\n"
                            f"City: {user.city}\n"
                            f"Contact: {user.phone}{' / ' + user.email if user.email else ''}\n"
                            f"Hospital: {blood_request.hospital_name}\n"
                            f"Required Date: {blood_request.required_date}\n\n"
                            f"If you're available, please contact the requester or hospital directly.\n"
                        ),
                        from_email=None,
                        recipient_list=[donor.email],
                        fail_silently=True,
                    )
            except Exception:
                pass
            return redirect('request_list')
    else:
        form = BloodRequestForm()
    return render(request, 'blood_app/request_form.html', {'form': form})


def request_list(request):
    requests = BloodRequest.objects.all()
    return render(request, 'blood_app/request_list.html', {'requests': requests})


@login_required
def hospital_dashboard(request):
    users = User.objects.all().order_by('name')
    requests = BloodRequest.objects.select_related('requester').order_by('-required_date')
    donations = BloodDonation.objects.select_related('donor').order_by('-donation_date')
    inventory = BloodInventory.objects.all()
    
    return render(request, 'blood_app/hospital_dashboard.html', {
        'users': users,
        'requests': requests,
        'donations': donations,
        'inventory': inventory,
        'request_statuses': ['Pending', 'Approved', 'Rejected', 'Fulfilled'],
    })


def donor_certificate(request, user_id):
    donor = get_object_or_404(User, id=user_id)
    if not donor.willing_to_donate:
        # Optional: could restrict certificate
        pass
    return render(request, 'blood_app/donor_certificate.html', {'donor': donor})


def certificate_lookup(request):
    if request.method != 'POST':
        return redirect('home')

    # Accept multiple search modes:
    # 1) By email (gmail or any email)
    # 2) By name + age
    # 3) Fallback: name + district (legacy)
    email = request.POST.get('email', '').strip()
    name = request.POST.get('name', '').strip()
    age_raw = request.POST.get('age', '').strip()
    district = request.POST.get('district', '').strip()
    taluk = request.POST.get('taluk', '').strip()

    matches = User.objects.none()

    # Prefer email if provided
    if email:
        matches = User.objects.filter(email__iexact=email)
        if not matches.exists():
            messages.error(request, 'No user found with that email.')
            return redirect('home')
    # Next, try name + age
    elif name and age_raw:
        try:
            age_val = int(age_raw)
        except ValueError:
            messages.error(request, 'Age must be a number.')
            return redirect('home')
        qs = User.objects.filter(name__icontains=name, age=age_val)
        if district:
            qs = qs.filter(district__icontains=district)
        if taluk:
            qs = qs.filter(taluk__icontains=taluk)
        matches = qs
        if not matches.exists():
            messages.error(request, 'No matching user found for the given name and age.')
            return redirect('home')
    # Legacy: name + district, or name only fallback
    elif name:
        qs = User.objects.filter(name__icontains=name)
        if district:
            qs = qs.filter(district__icontains=district)
        if taluk:
            qs = qs.filter(taluk__icontains=taluk)
        matches = qs
        if not matches.exists():
            messages.error(request, 'No matching user found. Please check the details provided.')
            return redirect('home')
    else:
        messages.error(request, 'Please provide email, or name with age.')
        return redirect('home')

    # One match → if user has donations, open latest donation certificate; else go to profile
    if matches.count() == 1:
        user = matches.first()
        latest_donation = user.blooddonation_set.order_by('-donation_date').first()
        if latest_donation:
            return redirect('donation_certificate', donation_id=latest_donation.id)
        return redirect('user_profile', user_id=user.id)

    return render(request, 'blood_app/certificate_results.html', {
        'results': matches.order_by('name'),
        'q_name': name,
        'q_district': district,
    })


@login_required
def update_request_status(request, request_id):
    if request.method != 'POST':
        return redirect('hospital_dashboard')
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    new_status = request.POST.get('status')
    if new_status:
        blood_request.status = new_status
        blood_request.save()
        messages.success(request, 'Request status updated.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('hospital_dashboard')


@login_required
def record_donation(request):
    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            
            # Update blood inventory
            try:
                inventory = BloodInventory.objects.get(blood_group=donation.blood_group)
                inventory.available_units += donation.units_donated
                inventory.save()
            except BloodInventory.DoesNotExist:
                BloodInventory.objects.create(
                    blood_group=donation.blood_group,
                    available_units=donation.units_donated
                )
            
            messages.success(request, f'Blood donation recorded successfully for {donation.donor.name}!')
            return redirect('donation_certificate', donation_id=donation.id)
    else:
        # Pre-fill donor if specified in URL
        initial = {}
        donor_id = request.GET.get('donor')
        if donor_id:
            try:
                donor = User.objects.get(id=donor_id)
                initial['donor'] = donor
                initial['blood_group'] = donor.blood_group
            except User.DoesNotExist:
                pass
        form = BloodDonationForm(initial=initial)
    
    return render(request, 'blood_app/record_donation.html', {'form': form})


def donation_certificate(request, donation_id):
    donation = get_object_or_404(BloodDonation, id=donation_id)
    return render(request, 'blood_app/blood_donation_certificate.html', {'donation': donation})


def donation_list(request):
    donations = BloodDonation.objects.select_related('donor').order_by('-donation_date')
    return render(request, 'blood_app/donation_list.html', {'donations': donations})


@login_required
def blood_inventory(request):
    if request.method == 'POST':
        form = BloodInventoryForm(request.POST)
        if form.is_valid():
            inventory, created = BloodInventory.objects.get_or_create(
                blood_group=form.cleaned_data['blood_group'],
                defaults={
                    'available_units': form.cleaned_data['available_units'],
                    'critical_level': form.cleaned_data['critical_level']
                }
            )
            if not created:
                inventory.available_units = form.cleaned_data['available_units']
                inventory.critical_level = form.cleaned_data['critical_level']
                inventory.save()
            messages.success(request, f'Blood inventory updated for {inventory.blood_group}')
            return redirect('blood_inventory')
    else:
        form = BloodInventoryForm()
    
    inventory_list = BloodInventory.objects.all().order_by('blood_group')
    return render(request, 'blood_app/blood_inventory.html', {
        'form': form,
        'inventory_list': inventory_list
    })


def add_emergency_contacts(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = user
            contact.save()
            messages.success(request, f'Emergency contact {contact.name} added successfully!')
            return redirect('user_profile', user_id=user.id)
    else:
        form = EmergencyContactForm()
    
    existing_contacts = user.emergency_contacts.all()
    return render(request, 'blood_app/add_emergency_contacts.html', {
        'form': form,
        'user': user,
        'existing_contacts': existing_contacts
    })


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    donations = user.blooddonation_set.all().order_by('-donation_date')
    emergency_contacts = user.emergency_contacts.all()
    
    return render(request, 'blood_app/user_profile.html', {
        'user': user,
        'donations': donations,
        'emergency_contacts': emergency_contacts
    })


def statistics(request):
    # Blood group distribution
    blood_group_stats = User.objects.filter(willing_to_donate=True).values('blood_group').annotate(
        count=Count('id')
    ).order_by('blood_group')
    
    # Donation statistics
    donation_stats = BloodDonation.objects.values('blood_group').annotate(
        total_units=Count('units_donated'),
        total_donations=Count('id')
    ).order_by('blood_group')
    
    # Monthly donation trends (improved for SQLite)
    monthly_donations = []
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for month in range(1, 13):
        count = BloodDonation.objects.filter(donation_date__month=month).count()
        monthly_donations.append({
            'month': month, 
            'month_name': month_names[month-1],
            'count': count
        })
    
    # Additional statistics for the template
    total_donors = User.objects.filter(willing_to_donate=True).count()
    total_donations = BloodDonation.objects.count()
    total_requests = BloodRequest.objects.count()
    
    # Get critical blood groups
    inventory = BloodInventory.objects.all()
    critical_blood_groups = [inv for inv in inventory if inv.is_critical()]
    
    return render(request, 'blood_app/statistics.html', {
        'blood_group_stats': blood_group_stats,
        'donation_stats': donation_stats,
        'monthly_donations': monthly_donations,
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_requests': total_requests,
        'critical_blood_groups': critical_blood_groups,
    })


def get_taluks(request):
    """AJAX view to get taluks for a selected district"""
    from django.http import JsonResponse
    
    district = request.GET.get('district')
    if district:
        taluks = User.get_taluks_by_district(district)
        return JsonResponse({'taluks': taluks})
    return JsonResponse({'taluks': []})
