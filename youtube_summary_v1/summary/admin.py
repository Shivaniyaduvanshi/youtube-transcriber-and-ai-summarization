from django.contrib import admin
from summary.models import User_data
# Register your models here.
class user_data_admin(admin.ModelAdmin):
    list_display = ('id','user','youtube_link','summary','ai_summary','created_at','updated_at')
admin.site.register(User_data,user_data_admin,)
