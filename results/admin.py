from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Student, Exam, Subject, Result, ResultSummary, GuardianLogin

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'father_name', 'class_name', 'section', 'is_active']
    search_fields = ['roll_number', 'name', 'father_name', 'student_id']
    list_filter = ['class_name', 'section', 'is_active', 'admission_year']
    list_editable = ['is_active']
    
    fieldsets = (
        ('ব্যক্তিগত তথ্য', {
            'fields': ('student_id', 'roll_number', 'name', 'father_name', 'mother_name', 
                      'date_of_birth', 'photo')
        }),
        ('একাডেমিক তথ্য', {
            'fields': ('class_name', 'section', 'admission_year')
        }),
        ('যোগাযোগ তথ্য', {
            'fields': ('phone', 'email', 'address', 'guardian_phone')
        }),
        ('অন্যান্য', {
            'fields': ('is_active',)
        }),
    )

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'academic_year', 'class_name', 'exam_date', 'is_published']
    list_filter = ['exam_type', 'academic_year', 'class_name', 'is_published']
    search_fields = ['name', 'academic_year', 'class_name']
    list_editable = ['is_published']
    date_hierarchy = 'exam_date'
    
    def save_model(self, request, obj, form, change):
        if obj.is_published and not obj.publish_date:
            from django.utils import timezone
            obj.publish_date = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'class_name', 'total_marks', 'pass_marks', 'is_elective']
    list_filter = ['category', 'class_name', 'is_elective']
    search_fields = ['name', 'code', 'class_name']
    ordering = ['class_name', 'name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'marks_obtained', 'grade', 'grade_point', 'is_passed']
    list_filter = ['exam', 'subject', 'grade', 'is_passed']
    search_fields = ['student__name', 'student__roll_number', 'subject__name']
    raw_id_fields = ['student', 'exam', 'subject']
    readonly_fields = ['grade', 'grade_point', 'is_passed']
    
    fieldsets = (
        ('পরীক্ষার্থীর তথ্য', {
            'fields': ('student', 'exam', 'subject')
        }),
        ('নম্বর ও ফলাফল', {
            'fields': ('marks_obtained', 'grade', 'grade_point', 'is_passed')
        }),
        ('মন্তব্য', {
            'fields': ('remarks',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'exam', 'subject')

@admin.register(ResultSummary)
class ResultSummaryAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'total_subjects', 'obtained_marks', 'percentage', 
                    'grade', 'cgpa', 'position', 'is_passed']
    list_filter = ['exam', 'grade', 'is_passed']
    search_fields = ['student__name', 'student__roll_number']
    raw_id_fields = ['student', 'exam']
    readonly_fields = ['total_grade_point', 'cgpa', 'percentage']
    
    fieldsets = (
        ('পরীক্ষার্থীর তথ্য', {
            'fields': ('student', 'exam')
        }),
        ('পরীক্ষার ফলাফল', {
            'fields': ('total_subjects', 'total_marks', 'obtained_marks', 'percentage')
        }),
        ('গ্রেড ও পয়েন্ট', {
            'fields': ('grade', 'total_grade_point', 'cgpa')
        }),
        ('মেধা তালিকা', {
            'fields': ('position', 'total_students', 'is_passed')
        }),
        ('মন্তব্য', {
            'fields': ('remarks',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'exam')

@admin.register(GuardianLogin)
class GuardianLoginAdmin(admin.ModelAdmin):
    list_display = ['student', 'username', 'email', 'phone', 'last_login', 'is_active']
    search_fields = ['student__name', 'username', 'email', 'phone']
    list_filter = ['is_active', 'last_login']
    raw_id_fields = ['student']
    
    fieldsets = (
        ('ছাত্র তথ্য', {
            'fields': ('student',)
        }),
        ('লগইন তথ্য', {
            'fields': ('username', 'password')
        }),
        ('যোগাযোগ তথ্য', {
            'fields': ('email', 'phone')
        }),
        ('অন্যান্য', {
            'fields': ('is_active', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['last_login']
    
    def save_model(self, request, obj, form, change):
        # যদি পাসওয়ার্ড পরিবর্তন করা হয় (নতুন বা আপডেট)
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)