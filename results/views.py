
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Avg, Count, Q
from django.template.loader import render_to_string
from django.conf import settings
import json
from .models import Student, Exam, Subject, Result, ResultSummary, GuardianLogin
from .forms import ResultSearchForm, GuardianLoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password, make_password
import datetime

def result_home(request):
    return render(request, 'results/result_home.html')

def check_result(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        exam_id = request.POST.get('exam')
        dob = request.POST.get('dob')
        
        try:
            student = Student.objects.get(roll_number=roll_number)
            
            if dob:
                try:
                    dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
                    if student.date_of_birth != dob_date:
                        messages.error(request, 'জন্ম তারিখ সঠিক নয়।')
                        return redirect('check_result')
                except:
                    pass
            
            exam = Exam.objects.get(id=exam_id, is_published=True)
            
            results = Result.objects.filter(student=student, exam=exam).select_related('subject')
            result_summary = ResultSummary.objects.filter(student=student, exam=exam).first()
            
            if not results:
                messages.warning(request, 'এই পরীক্ষার জন্য এখনো রেজাল্ট প্রকাশ করা হয়নি।')
                return redirect('check_result')
            
            context = {
                'student': student,
                'exam': exam,
                'results': results,
                'result_summary': result_summary,
            }
            
            return render(request, 'results/result_view.html', context)
            
        except Student.DoesNotExist:
            messages.error(request, 'এই রোল নম্বর দিয়ে কোন ছাত্র পাওয়া যায়নি।')
        except Exam.DoesNotExist:
            messages.error(request, 'এই পরীক্ষার রেজাল্ট এখনো প্রকাশ করা হয়নি।')
    
    exams = Exam.objects.filter(is_published=True).order_by('-exam_date')
    return render(request, 'results/check_result.html', {'exams': exams})

def result_view(request, result_id):
    result_summary = get_object_or_404(ResultSummary, id=result_id)
    student = result_summary.student
    exam = result_summary.exam
    results = Result.objects.filter(student=student, exam=exam).select_related('subject')
    
    context = {
        'student': student,
        'exam': exam,
        'results': results,
        'result_summary': result_summary,
    }
    
    return render(request, 'results/result_view.html', context)

def guardian_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            guardian = GuardianLogin.objects.get(username=username, is_active=True)
            
            if check_password(password, guardian.password):
                request.session['guardian_id'] = guardian.id
                request.session['student_id'] = guardian.student.id
                
                guardian.last_login = datetime.datetime.now()
                guardian.save()
                
                messages.success(request, 'সফলভাবে লগইন হয়েছে।')
                return redirect('guardian_dashboard')
            else:
                messages.error(request, 'পাসওয়ার্ড সঠিক নয়।')
        except GuardianLogin.DoesNotExist:
            messages.error(request, 'ব্যবহারকারী নাম সঠিক নয়।')
    
    return render(request, 'results/guardian_login.html')

def guardian_logout(request):
    if 'guardian_id' in request.session:
        del request.session['guardian_id']
    if 'student_id' in request.session:
        del request.session['student_id']
    
    messages.success(request, 'সফলভাবে লগআউট হয়েছে।')
    return redirect('guardian_login')

def guardian_dashboard(request):
    if 'guardian_id' not in request.session:
        messages.error(request, 'অনুগ্রহ করে প্রথমে লগইন করুন।')
        return redirect('guardian_login')
    
    try:
        guardian = GuardianLogin.objects.get(id=request.session['guardian_id'])
        student = guardian.student
        
        result_summaries = ResultSummary.objects.filter(student=student).select_related('exam').order_by('-exam__exam_date')
        
        # সহজ ভাবে পরিসংখ্যান বের করি
        total_exams = result_summaries.count()
        
        # সর্বোচ্চ শতকরা
        max_percentage = 0
        if result_summaries.exists():
            max_percentage = max([float(r.percentage) for r in result_summaries])
        
        # সর্বোচ্চ গ্রেড (A+ সবচেয়ে ভাল)
        grade_order = {'A+': 6, 'A': 5, 'A-': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
        best_grade = None
        best_grade_value = -1
        
        for summary in result_summaries:
            if summary.grade in grade_order and grade_order[summary.grade] > best_grade_value:
                best_grade = summary.grade
                best_grade_value = grade_order[summary.grade]
        
        # সর্বোচ্চ ক্রম (সবচেয়ে কম সংখ্যা)
        best_position = None
        for summary in result_summaries:
            if summary.position and (best_position is None or summary.position < best_position):
                best_position = summary.position
        
        # পারফরম্যান্স ডেটা তৈরি
        performance_data = []
        for summary in result_summaries:
            performance_data.append({
                'exam': summary.exam.name[:20] + ('...' if len(summary.exam.name) > 20 else ''),
                'percentage': float(summary.percentage),
                'grade': summary.grade,
                'position': summary.position,
            })
        
        context = {
            'guardian': guardian,
            'student': student,
            'result_summaries': result_summaries,
            'total_exams': total_exams,
            'max_percentage': max_percentage,
            'best_grade': best_grade,
            'best_position': best_position,
            'performance_data': performance_data,  # JSON না, সরাসরি লিস্ট
        }
        
        return render(request, 'results/guardian_dashboard.html', context)
        
    except GuardianLogin.DoesNotExist:
        messages.error(request, 'লগইন সেশন শেষ হয়েছে। অনুগ্রহ করে পুনরায় লগইন করুন।')
        return redirect('guardian_login')

def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, is_published=True)
    result_summaries = ResultSummary.objects.filter(exam=exam).select_related('student').order_by('position')
    
    context = {
        'exam': exam,
        'result_summaries': result_summaries,
    }
    
    return render(request, 'results/exam_results.html', context)

def api_check_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            roll_number = data.get('roll_number')
            exam_id = data.get('exam_id')
            
            student = Student.objects.get(roll_number=roll_number)
            exam = Exam.objects.get(id=exam_id, is_published=True)
            
            results = Result.objects.filter(student=student, exam=exam).select_related('subject')
            result_summary = ResultSummary.objects.filter(student=student, exam=exam).first()
            
            if not results:
                return JsonResponse({'error': 'রেজাল্ট পাওয়া যায়নি'}, status=404)
            
            result_data = {
                'student': {
                    'name': student.name,
                    'roll_number': student.roll_number,
                },
                'exam': {
                    'name': exam.name,
                },
                'results': [
                    {
                        'subject': result.subject.name,
                        'marks_obtained': float(result.marks_obtained),
                        'grade': result.grade,
                    }
                    for result in results
                ],
            }
            
            return JsonResponse(result_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST request প্রয়োজন'}, status=400)




