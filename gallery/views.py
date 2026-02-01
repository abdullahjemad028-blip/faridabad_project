
from django.shortcuts import render
from .models import GalleryCategory, GalleryImage

def gallery(request):
    categories = GalleryCategory.objects.all()
    all_images = GalleryImage.objects.all()
    
    context = {
        'categories': categories,
        'images': all_images,
    }
    return render(request, 'gallery/gallery.html', context)

def gallery_category(request, category_id):
    category = GalleryCategory.objects.get(id=category_id)
    images = GalleryImage.objects.filter(category=category)
    
    context = {
        'category': category,
        'images': images,
    }
    return render(request, 'gallery/gallery_category.html', context)