from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, BloodRequest, BloodDonation, BloodInventory, EmergencyContact


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'blood_group', 'city', 'district', 'taluk', 'age', 'gender', 'willing_to_donate', 'donation_count', 'photo_preview']
    list_filter = ['blood_group', 'district', 'taluk', 'gender', 'willing_to_donate', 'age']
    search_fields = ['name', 'email', 'phone']
    list_per_page = 25
    ordering = ['name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'age', 'gender', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Location', {
            'fields': ('city', 'district', 'taluk')
        }),
        ('Blood Donation', {
            'fields': ('blood_group', 'willing_to_donate')
        }),
    )
    
    def donation_count(self, obj):
        count = obj.get_donation_count()
        if count > 0:
            return format_html('<span class="badge bg-success">{}</span>', count)
        return format_html('<span class="badge bg-secondary">0</span>')
    donation_count.short_description = 'Donations'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:4px;" />', obj.photo.url)
        return format_html('<div style="width:50px;height:50px;background:#f8f9fa;border:1px solid #dee2e6;border-radius:4px;display:flex;align-items:center;justify-content:center;"><i class="fas fa-user text-muted"></i></div>')
    photo_preview.short_description = 'Photo'
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['requester_name', 'blood_group', 'hospital_name', 'required_date', 'status', 'requester_contact']
    list_filter = ['blood_group', 'status', 'required_date', 'requester__district']
    search_fields = ['requester__name', 'hospital_name']
    list_per_page = 25
    ordering = ['-required_date']
    
    def requester_name(self, obj):
        return obj.requester.name
    requester_name.short_description = 'Requester'
    
    def requester_contact(self, obj):
        return f"{obj.requester.phone}"
    requester_contact.short_description = 'Contact'
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }


@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'blood_group', 'donation_date', 'hospital_name', 'units_donated', 'donor_contact']
    list_filter = ['blood_group', 'donation_date', 'hospital_name', 'donor__district']
    search_fields = ['donor__name', 'hospital_name']
    list_per_page = 25
    ordering = ['-donation_date']
    
    def donor_name(self, obj):
        return obj.donor.name
    donor_name.short_description = 'Donor'
    
    def donor_contact(self, obj):
        return f"{obj.donor.phone}"
    donor_contact.short_description = 'Contact'
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ['blood_group', 'available_units', 'critical_level', 'status_indicator', 'last_updated']
    list_filter = ['blood_group']
    search_fields = ['blood_group']
    list_per_page = 25
    ordering = ['blood_group']
    
    def status_indicator(self, obj):
        if obj.available_units == 0:
            return format_html('<span class="status-out">Out of Stock</span>')
        elif obj.is_critical():
            return format_html('<span class="status-critical">Critical</span>')
        else:
            return format_html('<span class="status-available">Available</span>')
    status_indicator.short_description = 'Status'
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'name', 'relationship', 'phone', 'email']
    list_filter = ['relationship', 'user__district']
    search_fields = ['user__name', 'name', 'phone']
    list_per_page = 25
    ordering = ['user__name', 'name']
    
    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = 'User'
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }


# Customize Admin Site
admin.site.site_header = "Blood Donation Management System"
admin.site.site_title = "Blood Donation Admin"
admin.site.index_title = "Welcome to Blood Donation Administration"

# Custom Admin Actions
@admin.action(description="Mark selected users as willing to donate")
def make_willing_to_donate(modeladmin, request, queryset):
    queryset.update(willing_to_donate=True)
    modeladmin.message_user(request, f"{queryset.count()} users marked as willing to donate.")

@admin.action(description="Mark selected users as not willing to donate")
def make_not_willing_to_donate(modeladmin, request, queryset):
    queryset.update(willing_to_donate=False)
    modeladmin.message_user(request, f"{queryset.count()} users marked as not willing to donate.")

# Add actions to UserAdmin
UserAdmin.actions = [make_willing_to_donate, make_not_willing_to_donate]
