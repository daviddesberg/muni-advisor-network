from django.contrib import admin
from .models import Advisor, Delegate, School


class AdvisorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'school',
        'email',
        'mobile_phone_number',
        'work_phone_number',
        'created_at',
        'updated_at'
    ]


class AdvisorInline(admin.TabularInline):
    model = Advisor


class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'paid_school_fee',
        'paid_delegate_fees', 'transportation_required',
        'interested_crisis_committees',
        'interested_ipd_positions',
        'delegate_count_estimate',
        'marked_paid_at',
        'created_at',
        'updated_at',
        'additional_registration_notes'
    ]

    inlines = [
        AdvisorInline
    ]


class DelegateAdmin(admin.ModelAdmin):
    pass


admin.site.register(School, SchoolAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Delegate, DelegateAdmin)

admin.site.site_title = 'MUNI Advisor Network'
admin.site.site_header = 'MUNI Advisor Network'
