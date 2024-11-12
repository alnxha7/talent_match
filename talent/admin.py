from django.contrib import admin
from .models import UserProfile, Aspirants, Company, CompanyJobs


@admin.register(Aspirants)
class AspirantsAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number')
    search_fields = ('username', 'email')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'address', 'approved')
    search_fields = ('username', 'email')
    list_filter = ('approved',)

    actions = ['approve_companies', 'reject_companies']

    def approve_companies(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected companies have been approved.")

    def reject_companies(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected companies have been rejected.")

    approve_companies.short_description = "Approve selected companies"
    reject_companies.short_description = "Reject selected companies"


