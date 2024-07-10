from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_data(models.Model):
    # class Meta:
    #     __tablename__='user_data'
    id=models.AutoField(primary_key=True)
    youtube_link=models.TextField()
    summary=models.TextField()
    ai_summary=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
    class Meta:
        db_table='user_data'
        verbose_name='User Data'
        verbose_name_plural='User Data'
