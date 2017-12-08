from django.contrib import admin
from .models import Advisor, Delegate, School, PositionPaper, PrintDocument
from totalsum.admin import TotalsumAdmin


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


class DelegateInline(admin.TabularInline):
    model = Delegate


class SchoolAdmin(TotalsumAdmin):
    # actual_delegate_count.short_description = "Actual Delegate Count"
    totalsum_list = ['delegate_count_estimate', 'actual_delegate_count']

    list_display = [
        'name', 'paid_school_fee',
        'paid_delegate_fees', 'transportation_required',
        'interested_crisis_committees',
        'interested_ipd_positions',
        'delegate_count_estimate',
        'actual_delegate_count',
        'marked_paid_at',
        'created_at',
        'updated_at',
        'additional_registration_notes'
    ]

    inlines = [
        AdvisorInline,
        DelegateInline
    ]


class DelegateAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'school',
        'committee',
        'position'
    ]


class PositionPaperAdmin(admin.ModelAdmin):
    list_display = [
        'delegate',
        'created_at',
        'updated_at'
    ]


class PrintDocumentAdmin(admin.ModelAdmin):
    list_display = ['processed', 'created_at', 'committee', 'num_copies', 'comments']

admin.site.register(School, SchoolAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Delegate, DelegateAdmin)
admin.site.register(PositionPaper, PositionPaperAdmin)
admin.site.register(PrintDocument, PrintDocumentAdmin)

admin.site.site_title = 'MUNI Advisor Network'
admin.site.site_header = 'MUNI Advisor Network'
