from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import InstitutionInfo, Program, Teacher, Notice, ContactMessage
from gallery.models import GalleryImage
from notice.models import Event
from django.utils import timezone

def home(request):
    institution = InstitutionInfo.objects.first()
    notices = Notice.objects.filter(valid_until__gte=timezone.now().date())[:5]
    featured_images = GalleryImage.objects.filter(is_featured=True)[:6]
    events = Event.objects.filter(event_date__gte=timezone.now().date())[:3]
    
    context = {
        'institution': institution,
        'notices': notices,
        'featured_images': featured_images,
        'events': events,
    }
    return render(request, 'main/home.html', context)

def about(request):
    institution = InstitutionInfo.objects.first()
    teachers = Teacher.objects.filter(is_active=True)
    
    context = {
        'institution': institution,
        'teachers': teachers,
    }
    return render(request, 'main/about.html', context)

def programs(request):
    programs_list = Program.objects.filter(is_active=True)
    
    context = {
        'programs': programs_list,
    }
    return render(request, 'main/programs.html', context)

def teachers(request):
    teachers_list = Teacher.objects.filter(is_active=True)
    
    context = {
        'teachers': teachers_list,
    }
    return render(request, 'main/teachers.html', context)

def contact(request):
    institution = InstitutionInfo.objects.first()
    
    context = {
        'institution': institution,
    }
    return render(request, 'main/contact.html', context)

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        return render(request, 'main/contact_success.html')
    
    return redirect('contact')