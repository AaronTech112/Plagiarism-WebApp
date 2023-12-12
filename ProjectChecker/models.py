from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name   

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True, )
    matric_number = models.CharField(unique=True,null=True,max_length=255, default=None)
    staff_id_number = models.CharField(unique=True,null=True,max_length=255, default=None)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='students', null=True,default=None)
    phone_number = models.IntegerField(null=True, unique=True)
    profile_pic = models.ImageField(default="avatar.png",upload_to = 'img', null = True,)
    GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('rather_not_say', 'Rather not say'),
    )
    gender = models.CharField(max_length=100,choices=GENDER_CHOICES, default='rather_not_say')
    STATUS = (
        ('lecturer','lecturer'),
        ('student','student'),
    )
    status = models.CharField(max_length=100, choices=STATUS, default='student')
    
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']
 

    def __str__(self):
        return self.email

class Project(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    author = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='projects')
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='projects')
    SESSION_CHOICES = (
        ('2022/2023','2022/2023'),
        ('2021/2022','2021/2022'),
        ('2020/2021','2020/2021'),
        ('2019/2020','2019/2020'),
        ('2018/2019','2018/2019'),
   
    )
    session = models.CharField(max_length=200,choices=SESSION_CHOICES,default='2022/2023')
    STATUS = (
        ('approved','approved'),
        ('declined','declined'),
        ('pending','pending'),
    )
    status = models.CharField(max_length=100, choices=STATUS, default='pending')

    def __str__(self):
        return self.title
    