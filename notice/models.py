
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="ইভেন্টের নাম")
    description = models.TextField(verbose_name="বর্ণনা")
    event_date = models.DateField(verbose_name="ইভেন্ট তারিখ")
    event_time = models.TimeField(verbose_name="সময়")
    venue = models.CharField(max_length=200, verbose_name="স্থান")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "ইভেন্ট"
        verbose_name_plural = "ইভেন্টসমূহ"