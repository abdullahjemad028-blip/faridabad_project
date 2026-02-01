from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    CLASS_CHOICES = [
        # মক্তব বিভাগ (৫ বছর - প্রাইমারী স্তর)
        ('মক্তব ১ম বর্ষ', 'মক্তব ১ম বর্ষ'),
        ('মক্তব ২য় বর্ষ', 'মক্তব ২য় বর্ষ'),
        ('মক্তব ৩য় বর্ষ', 'মক্তব ৩য় বর্ষ'),
        ('মক্তব ৪র্থ বর্ষ', 'মক্তব ৪র্থ বর্ষ'),
        ('মক্তব ৫ম বর্ষ', 'মক্তব ৫ম বর্ষ'),
        
        # হিফয বিভাগ
        ('হিফয বিভাগ', 'হিফয বিভাগ'),
        
        # মারহালা ইবতিদাইয়্যাহ (২ বছর - নিম্ন মাধ্যমিক)
        ('মারহালা ইবতিদাইয়্যাহ ১ম বর্ষ', 'মারহালা ইবতিদাইয়্যাহ ১ম বর্ষ'),
        ('মারহালা ইবতিদাইয়্যাহ ২য় বর্ষ', 'মারহালা ইবতিদাইয়্যাহ ২য় বর্ষ'),
        
        # মারহালা মুতাওয়াসসিতা (৪ বছর - মাধ্যমিক)
        ('মারহালা মুতাওয়াসসিতা ১ম বর্ষ', 'মারহালা মুতাওয়াসসিতা ১ম বর্ষ'),
        ('মারহালা মুতাওয়াসসিতা ২য় বর্ষ', 'মারহালা মুতাওয়াসসিতা ২য় বর্ষ'),
        ('মারহালা মুতাওয়াসসিতা ৩য় বর্ষ', 'মারহালা মুতাওয়াসসিতা ৩য় বর্ষ'),
        ('মারহালা মুতাওয়াসসিতা ৪র্থ বর্ষ', 'মারহালা মুতাওয়াসসিতা ৪র্থ বর্ষ'),
        
        # মারহালা সানাবিয়া উলইয়া (২ বছর - উচ্চ মাধ্যমিক)
        ('মারহালা সানাবিয়া উলইয়া ১ম বর্ষ', 'মারহালা সানাবিয়া উলইয়া ১ম বর্ষ'),
        ('মারহালা সানাবিয়া উলইয়া ২য় বর্ষ', 'মারহালা সানাবিয়া উলইয়া ২য় বর্ষ'),
        
        # মারহালা ফজিলত (২ বছর - স্নাতক)
        ('মারহালা ফজিলত ১ম বর্ষ', 'মারহালা ফজিলত ১ম বর্ষ'),
        ('মারহালা ফজিলত ২য় বর্ষ', 'মারহালা ফজিলত ২য় বর্ষ'),
        
        # মারহালা তাকমিল (১ বছর - মাস্টার্স / দাওরায়ে হাদীস)
        ('মারহালা তাকমিল', 'মারহালা তাকমিল (দাওরায়ে হাদীস)'),
        
        # ইফতা বিভাগ (২ বছর)
        ('ইফতা ১ম বর্ষ', 'ইফতা ১ম বর্ষ'),
        ('ইফতা ২য় বর্ষ', 'ইফতা ২য় বর্ষ'),
    ]
    
    SECTION_CHOICES = [
        ('ক', 'ক'),
        ('খ', 'খ'),
        ('গ', 'গ'),
        ('ঘ', 'ঘ'),
    ]
    
    student_id = models.CharField(max_length=20, unique=True, verbose_name="ছাত্র আইডি")
    roll_number = models.CharField(max_length=20, unique=True, verbose_name="রোল নং")
    name = models.CharField(max_length=100, verbose_name="ছাত্রের নাম")
    father_name = models.CharField(max_length=100, verbose_name="পিতার নাম")
    mother_name = models.CharField(max_length=100, verbose_name="মাতার নাম")
    date_of_birth = models.DateField(verbose_name="জন্ম তারিখ")
    class_name = models.CharField(max_length=100, choices=CLASS_CHOICES, verbose_name="শ্রেণী")
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, verbose_name="বিভাগ", blank=True)
    admission_year = models.IntegerField(verbose_name="ভর্তির বছর")
    phone = models.CharField(max_length=15, verbose_name="ফোন নম্বর", blank=True)
    email = models.EmailField(verbose_name="ইমেইল", blank=True)
    address = models.TextField(verbose_name="ঠিকানা")
    guardian_phone = models.CharField(max_length=15, verbose_name="অভিভাবকের ফোন")
    photo = models.ImageField(upload_to='students/', verbose_name="ছবি", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.roll_number} ({self.class_name})"
    
    class Meta:
        verbose_name = "ছাত্র"
        verbose_name_plural = "ছাত্রবৃন্দ"
        ordering = ['class_name', 'roll_number']

class Exam(models.Model):
    EXAM_TYPES = [
        ('মাসিক পরীক্ষা', 'মাসিক পরীক্ষা'),
        ('ত্রৈমাসিক পরীক্ষা', 'ত্রৈমাসিক পরীক্ষা'),
        ('অর্ধ-বার্ষিক পরীক্ষা', 'অর্ধ-বার্ষিক পরীক্ষা'),
        ('বার্ষিক পরীক্ষা', 'বার্ষিক পরীক্ষা'),
        ('সমাপনী পরীক্ষা', 'সমাপনী পরীক্ষা'),
        ('অন্যান্য', 'অন্যান্য'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="পরীক্ষার নাম")
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPES, verbose_name="পরীক্ষার ধরণ")
    academic_year = models.CharField(max_length=20, verbose_name="শিক্ষাবর্ষ")
    class_name = models.CharField(max_length=100, verbose_name="শ্রেণী")
    exam_date = models.DateField(verbose_name="পরীক্ষার তারিখ")
    total_marks = models.IntegerField(verbose_name="মোট নম্বর", default=100)
    pass_marks = models.IntegerField(verbose_name="পাশ নম্বর", default=40)
    is_published = models.BooleanField(default=False, verbose_name="প্রকাশিত")
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name="প্রকাশের তারিখ")
    
    def __str__(self):
        return f"{self.name} - {self.academic_year} ({self.class_name})"
    
    class Meta:
        verbose_name = "পরীক্ষা"
        verbose_name_plural = "পরীক্ষাসমূহ"
        ordering = ['-exam_date']

class Subject(models.Model):
    SUBJECT_CATEGORIES = [
        # মক্তব বিভাগের বিষয়
        ('কুরআন', 'কুরআন'),
        ('বাংলা', 'বাংলা'),
        ('ইংরেজি', 'ইংরেজি'),
        ('অংক', 'অংক (গণিত)'),
        ('ভূগোল', 'ভূগোল'),
        ('ইতিহাস', 'ইতিহাস'),
        ('উর্দু', 'উর্দু'),
        ('ফার্সি', 'ফার্সি'),
        ('মাসায়েল', 'জরুরি মাসায়েল'),
        
        # আরবী বিভাগের বিষয়
        ('সরফ', 'ইলমে সরফ (আরবী ব্যাকরণ)'),
        ('নাহু', 'ইলমে নাহু (আরবী ব্যাকরণ)'),
        ('আরবী সাহিত্য', 'আরবী সাহিত্য'),
        ('ফিকহ', 'ফিকহ'),
        ('উসূলে ফিকহ', 'উসূলে ফিকহ'),
        ('মানতেক', 'ইলমে মানতেক (যুক্তিবিদ্যা)'),
        ('অলঙ্কারশাস্ত্র', 'অলঙ্কারশাস্ত্র'),
        ('ফারায়েজ', 'ফারায়েজ'),
        
        # উচ্চতর বিষয়
        ('তাফসীর', 'তাফসীর'),
        ('উসূলে তাফসীর', 'উসূলে তাফসীর'),
        ('হাদীস', 'হাদীস'),
        ('উলূমে হাদীস', 'উলূমে হাদীস'),
        ('আকাইদ', 'ইসলামী আকাইদ'),
        ('ইসলামী ইতিহাস', 'ইসলামী ইতিহাস'),
        
        # হাদীসের কিতাব (তাকমিল/দাওরায়ে হাদীস)
        ('বুখারি', 'সহীহ বুখারি'),
        ('মুসলিম', 'সহীহ মুসলিম'),
        ('তিরমিযী', 'জামে তিরমিযী'),
        ('আবূ দাউদ', 'সুনানে আবূ দাউদ'),
        ('নাসাঈ', 'সুনানে নাসাঈ'),
        ('ইবনে মাজাহ', 'সুনানে ইবনে মাজাহ'),
        ('মুয়াত্তা মুহাম্মদ', 'মুয়াত্তা মুহাম্মদ'),
        ('মুয়াত্তা মালেক', 'মুয়াত্তা মালেক'),
        ('শরহু মাআনিল আসার', 'শরহু মাআনিল আসার'),
        ('শামায়েলে তিরমিযী', 'শামায়েলে তিরমিযী'),
        
        # অন্যান্য
        ('সাধারণ জ্ঞান', 'সাধারণ জ্ঞান'),
        ('অন্যান্য', 'অন্যান্য'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="বিষয়ের নাম")
    code = models.CharField(max_length=20, unique=True, verbose_name="বিষয় কোড")
    category = models.CharField(max_length=50, choices=SUBJECT_CATEGORIES, verbose_name="বিষয় বিভাগ")
    class_name = models.CharField(max_length=100, verbose_name="শ্রেণী")
    total_marks = models.IntegerField(verbose_name="মোট নম্বর", default=100)
    pass_marks = models.IntegerField(verbose_name="পাশ নম্বর", default=40)
    is_elective = models.BooleanField(default=False, verbose_name="নির্বাচনী")
    
    def __str__(self):
        return f"{self.name} ({self.code}) - {self.class_name}"
    
    class Meta:
        verbose_name = "বিষয়"
        verbose_name_plural = "বিষয়সমূহ"
        ordering = ['class_name', 'name']

class Result(models.Model):
    GRADES = [
        ('ممتاز', 'ممتاز (মুমতাজ - ৮০-১০০)'),
        ('جيد جدا', 'جيد جدا (জাইয়্যেদ জিদ্দান - ৭০-৭৯)'),
        ('جيد', 'جيد (জাইয়্যেদ - ৬০-৬৯)'),
        ('مقبول', 'مقبول (মাকবুল - ৫০-৫৯)'),
        ('حسن', 'حسن (হাসান - ৪০-৪৯)'),
        ('ضعيف', 'ضعيف (জয়ীফ - ৩৩-৩৯)'),
        ('راسب', 'راسب (রাসিব/অকৃতকার্য - ০-৩২)'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="ছাত্র", related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="পরীক্ষা", related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="বিষয়", related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="প্রাপ্ত নম্বর")
    grade = models.CharField(max_length=20, choices=GRADES, verbose_name="গ্রেড")
    grade_point = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="গ্রেড পয়েন্ট")
    is_passed = models.BooleanField(default=True, verbose_name="পাশ")
    remarks = models.TextField(verbose_name="মন্তব্য", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate grade based on marks
        marks = float(self.marks_obtained)
        total_marks = float(self.subject.total_marks)
        percentage = (marks / total_marks) * 100
        
        if percentage >= 80:
            self.grade = 'ممتاز'
            self.grade_point = 5.00
        elif percentage >= 70:
            self.grade = 'جيد جدا'
            self.grade_point = 4.00
        elif percentage >= 60:
            self.grade = 'جيد'
            self.grade_point = 3.50
        elif percentage >= 50:
            self.grade = 'مقبول'
            self.grade_point = 3.00
        elif percentage >= 40:
            self.grade = 'حسن'
            self.grade_point = 2.00
        elif percentage >= 33:
            self.grade = 'ضعيف'
            self.grade_point = 1.00
        else:
            self.grade = 'راسب'
            self.grade_point = 0.00
            self.is_passed = False
        
        # Check if marks are below pass marks
        if marks < self.subject.pass_marks:
            self.is_passed = False
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.grade}"
    
    class Meta:
        verbose_name = "রেজাল্ট"
        verbose_name_plural = "রেজাল্টসমূহ"
        unique_together = ['student', 'exam', 'subject']
        ordering = ['-exam__exam_date', 'student__roll_number']

class ResultSummary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="ছাত্র", related_name='summaries')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="পরীক্ষা", related_name='summaries')
    total_subjects = models.IntegerField(verbose_name="মোট বিষয়")
    total_marks = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="মোট নম্বর")
    obtained_marks = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="প্রাপ্ত নম্বর")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="শতকরা")
    grade = models.CharField(max_length=20, verbose_name="গ্রেড")
    total_grade_point = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="মোট গ্রেড পয়েন্ট")
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="CGPA")
    position = models.IntegerField(verbose_name="ক্রম", null=True, blank=True)
    total_students = models.IntegerField(verbose_name="মোট ছাত্র", default=0)
    is_passed = models.BooleanField(default=True, verbose_name="সফল")
    remarks = models.TextField(verbose_name="মন্তব্য", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.exam.name} - {self.grade}"
    
    class Meta:
        verbose_name = "রেজাল্ট সারসংক্ষেপ"
        verbose_name_plural = "রেজাল্ট সারসংক্ষেপসমূহ"
        unique_together = ['student', 'exam']
        ordering = ['-exam__exam_date', 'position']

class GuardianLogin(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, verbose_name="ছাত্র", related_name='guardian_login')
    username = models.CharField(max_length=50, unique=True, verbose_name="ব্যবহারকারীর নাম")
    password = models.CharField(max_length=100, verbose_name="পাসওয়ার্ড")
    email = models.EmailField(verbose_name="ইমেইল")
    phone = models.CharField(max_length=15, verbose_name="ফোন")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="সর্বশেষ লগইন")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - অভিভাবক ({self.username})"
    
    class Meta:
        verbose_name = "অভিভাবক লগইন"
        verbose_name_plural = "অভিভাবক লগইনসমূহ"