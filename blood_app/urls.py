from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # Ensure default Django post-login profile URL redirects to home
    path('accounts/profile/', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('register/', views.register_user, name='register'),
    path('donors/', views.donor_list, name='donor_list'),
    path('request/<int:user_id>/', views.request_blood, name='request_blood'),
    path('requests/', views.request_list, name='request_list'),
    path('hospital/', views.hospital_dashboard, name='hospital_dashboard'),
    path('certificate/<int:user_id>/', views.donor_certificate, name='donor_certificate'),
    path('certificate/lookup/', views.certificate_lookup, name='certificate_lookup'),
    path('requests/<int:request_id>/status/', views.update_request_status, name='update_request_status'),
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/record/', views.record_donation, name='record_donation'),
    path('donations/<int:donation_id>/certificate/', views.donation_certificate, name='donation_certificate'),
    path('inventory/', views.blood_inventory, name='blood_inventory'),
    path('user/<int:user_id>/emergency-contacts/', views.add_emergency_contacts, name='add_emergency_contacts'),
    path('user/<int:user_id>/profile/', views.user_profile, name='user_profile'),
    path('statistics/', views.statistics, name='statistics'),
    path('get-taluks/', views.get_taluks, name='get_taluks'),
]


