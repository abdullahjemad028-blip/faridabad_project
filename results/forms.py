from django import forms
from .models import Student, Exam, Result, Subject

class ResultSearchForm(forms.Form):
    """রেজাল্ট সার্চ ফর্ম"""
    roll_number = forms.CharField(
        max_length=20,
        label='রোল নম্বর',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'রোল নম্বর দিন',
            'required': True
        })
    )
    
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.filter(is_published=True).order_by('-exam_date'),
        label='পরীক্ষা নির্বাচন করুন',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        empty_label="পরীক্ষা নির্বাচন করুন"
    )
    
    date_of_birth = forms.DateField(
        label='জন্ম তারিখ (ঐচ্ছিক)',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'yyyy-mm-dd'
        }),
        help_text='নিরাপত্তার জন্য জন্ম তারিখ প্রদান করুন'
    )
    
    def clean_roll_number(self):
        """রোল নম্বর validate করুন"""
        roll_number = self.cleaned_data.get('roll_number')
        if roll_number:
            roll_number = roll_number.strip()
        return roll_number

class GuardianLoginForm(forms.Form):
    """অভিভাবক লগইন ফর্ম"""
    username = forms.CharField(
        max_length=50,
        label='ব্যবহারকারীর নাম',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ব্যবহারকারীর নাম',
            'required': True,
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        label='পাসওয়ার্ড',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'পাসওয়ার্ড',
            'required': True,
            'autocomplete': 'current-password'
        })
    )
    
    remember_me = forms.BooleanField(
        label='আমাকে মনে রাখুন',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean_username(self):
        """ব্যবহারকারীর নাম validate করুন"""
        username = self.cleaned_data.get('username')
        if username:
            username = username.strip().lower()
        return username

class BulkResultUploadForm(forms.Form):
    """বাল্ক রেজাল্ট আপলোড ফর্ম"""
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all().order_by('-exam_date'),
        label='পরীক্ষা',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        empty_label="পরীক্ষা নির্বাচন করুন"
    )
    
    excel_file = forms.FileField(
        label='এক্সেল ফাইল',
        help_text='এক্সেল ফাইল আপলোড করুন (.xlsx বা .xls ফরম্যাট)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls',
            'required': True
        })
    )
    
    def clean_excel_file(self):
        """এক্সেল ফাইল validate করুন"""
        excel_file = self.cleaned_data.get('excel_file')
        
        if excel_file:
            # ফাইল এক্সটেনশন চেক করুন
            file_name = excel_file.name
            if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
                raise forms.ValidationError('শুধুমাত্র .xlsx বা .xls ফাইল আপলোড করুন।')
            
            # ফাইল সাইজ চেক করুন (সর্বোচ্চ ৫ MB)
            if excel_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('ফাইল সাইজ ৫ MB এর বেশি হতে পারবে না।')
        
        return excel_file

class ResultEntryForm(forms.ModelForm):
    """একক রেজাল্ট এন্ট্রি ফর্ম"""
    class Meta:
        model = Result
        fields = ['student', 'exam', 'subject', 'marks_obtained', 'remarks']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'exam': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'প্রাপ্ত নম্বর',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'মন্তব্য (ঐচ্ছিক)'
            })
        }
        labels = {
            'student': 'ছাত্র',
            'exam': 'পরীক্ষা',
            'subject': 'বিষয়',
            'marks_obtained': 'প্রাপ্ত নম্বর',
            'remarks': 'মন্তব্য'
        }
    
    def clean_marks_obtained(self):
        """প্রাপ্ত নম্বর validate করুন"""
        marks = self.cleaned_data.get('marks_obtained')
        subject = self.cleaned_data.get('subject')
        
        if marks and subject:
            if marks < 0:
                raise forms.ValidationError('নম্বর ০ এর কম হতে পারবে না।')
            if marks > subject.total_marks:
                raise forms.ValidationError(
                    f'নম্বর {subject.total_marks} এর বেশি হতে পারবে না।'
                )
        
        return marks

class ClassFilterForm(forms.Form):
    """শ্রেণী ফিল্টার ফর্ম"""
    class_name = forms.ChoiceField(
        label='শ্রেণী',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    section = forms.ChoiceField(
        label='বিভাগ',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ডায়নামিক শ্রেণী choices
        from .models import Student
        classes = Student.objects.values_list('class_name', 'class_name').distinct().order_by('class_name')
        self.fields['class_name'].choices = [('', 'সকল শ্রেণী')] + list(classes)
        
        # ডায়নামিক বিভাগ choices
        sections = Student.objects.values_list('section', 'section').distinct().order_by('section')
        self.fields['section'].choices = [('', 'সকল বিভাগ')] + list(sections)

class ExamFilterForm(forms.Form):
    """পরীক্ষা ফিল্টার ফর্ম"""
    exam_type = forms.ChoiceField(
        label='পরীক্ষার ধরণ',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    academic_year = forms.ChoiceField(
        label='শিক্ষাবর্ষ',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class_name = forms.ChoiceField(
        label='শ্রেণী',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ডায়নামিক choices
        exam_types = Exam.objects.values_list('exam_type', 'exam_type').distinct()
        self.fields['exam_type'].choices = [('', 'সকল ধরণ')] + list(exam_types)
        
        academic_years = Exam.objects.values_list('academic_year', 'academic_year').distinct().order_by('-academic_year')
        self.fields['academic_year'].choices = [('', 'সকল বছর')] + list(academic_years)
        
        classes = Exam.objects.values_list('class_name', 'class_name').distinct().order_by('class_name')
        self.fields['class_name'].choices = [('', 'সকল শ্রেণী')] + list(classes)

class StudentSearchForm(forms.Form):
    """ছাত্র সার্চ ফর্ম"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        label='সার্চ করুন',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'নাম, রোল নম্বর বা আইডি দিয়ে সার্চ করুন'
        })
    )
    
    class_name = forms.ChoiceField(
        label='শ্রেণী',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    is_active = forms.ChoiceField(
        label='স্ট্যাটাস',
        required=False,
        choices=[
            ('', 'সকল'),
            ('True', 'সক্রিয়'),
            ('False', 'নিষ্ক্রিয়')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ডায়নামিক শ্রেণী choices
        classes = Student.objects.values_list('class_name', 'class_name').distinct().order_by('class_name')
        self.fields['class_name'].choices = [('', 'সকল শ্রেণী')] + list(classes)