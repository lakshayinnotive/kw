from django.contrib import admin
from .models import LoginData, Forget, MainData, NewsLetter, CustomerReview, HeadCarousel
# Register your models here.


admin.site.register(LoginData)
admin.site.register(Forget)
admin.site.register(MainData)
admin.site.register(NewsLetter)
admin.site.register(CustomerReview)
admin.site.register(HeadCarousel)
# admin.site.register(Profile)