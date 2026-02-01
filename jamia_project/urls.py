from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('gallery/', include('gallery.urls')),
    path('notice/', include('notice.urls')),
    path('results/', include('results.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "জামিয়া আরাবিয়া ইমদাদুল উলুম ফারিদাবাদ"
admin.site.site_title = "এডমিন প্যানেল"
admin.site.index_title = "স্বাগতম এডমিন প্যানেলে"



