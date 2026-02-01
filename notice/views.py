
from django.shortcuts import render
from django.utils import timezone
from main.models import Notice
from .models import Event

def all_notices(request):
    notices = Notice.objects.filter(valid_until__gte=timezone.now().date())
    
    context = {
        'notices': notices,
    }
    return render(request, 'notice/all_notices.html', context)

def events(request):
    upcoming_events = Event.objects.filter(event_date__gte=timezone.now().date())
    past_events = Event.objects.filter(event_date__lt=timezone.now().date())
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'notice/events.html', context)

def notice_detail(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    
    context = {
        'notice': notice,
    }
    return render(request, 'notice/notice_detail.html', context)