from django.contrib import admin
from .models import InstitutionInfo, Program, Teacher, Notice, ContactMessage

@admin.register(InstitutionInfo)
class InstitutionInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'established_date', 'phone', 'email']
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('name', 'description', 'history', 'established_date')
        }),
        ('মিশন ও ভিশন', {
            'fields': ('mission', 'vision')
        }),
        ('যোগাযোগ', {
            'fields': ('address', 'phone', 'email')
        }),
    )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'program_type', 'duration', 'is_active']
    list_filter = ['program_type', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'joining_date', 'is_active']
    list_filter = ['is_active', 'designation']
    search_fields = ['name', 'qualifications']
    list_editable = ['is_active']
    fieldsets = (
        ('ব্যক্তিগত তথ্য', {
            'fields': ('name', 'photo', 'designation')
        }),
        ('যোগ্যতা ও অভিজ্ঞতা', {
            'fields': ('qualifications', 'experience')
        }),
        ('যোগাযোগ', {
            'fields': ('phone', 'email')
        }),
        ('অন্যান্য', {
            'fields': ('joining_date', 'is_active')
        }),
    )

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_posted', 'valid_until', 'is_important']
    list_filter = ['is_important', 'date_posted']
    search_fields = ['title', 'content']
    list_editable = ['is_important']
    date_hierarchy = 'date_posted'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'date_sent', 'is_read']
    list_filter = ['is_read', 'date_sent']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'date_sent']