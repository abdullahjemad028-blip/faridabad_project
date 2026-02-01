from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="ক্যাটেগরির নাম")
    description = models.TextField(verbose_name="বর্ণনা", blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "গ্যালারি ক্যাটেগরি"
        verbose_name_plural = "গ্যালারি ক্যাটেগরিসমূহ"

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="শিরোনাম")
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, verbose_name="ক্যাটেগরি")
    image = models.ImageField(upload_to='gallery/', verbose_name="ছবি")
    description = models.TextField(verbose_name="বর্ণনা", blank=True)
    date_taken = models.DateField(verbose_name="তোলার তারিখ")
    is_featured = models.BooleanField(default=False, verbose_name="প্রধান পাতায় দেখান")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "গ্যালারি ছবি"
        verbose_name_plural = "গ্যালারি ছবিসমূহ"
