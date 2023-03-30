from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #姓名
    real_name = models.CharField(max_length=40,blank=True)
    #部门
    department = models.CharField(max_length=40,blank=True)
    #职位
    position = models.CharField(max_length=40,blank=True)
    #学校
    college = models.CharField(max_length=40,blank=True)
    #头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
     # 个人简介
    bio = models.TextField(max_length=500, blank=True)
    
    is_engineer = models.BooleanField(default=False)


    def __str__(self):
        return 'user {}'.format(self.user.username)

