from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Campos personalizados
    ROLE_CHOICES = (
    ('student', 'Student'),
    ('professor', 'Professor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    nusp = models.CharField(max_length=20, unique=True, null=True, blank=True)
    # Campos de Aluno
    course = models.CharField(max_length=100, null=True, blank=True)
    ideal_period = models.IntegerField(null=True, blank=True)
    curriculum_base64 = models.TextField(null=True, blank=True)
    curriculum_filename = models.CharField(max_length=255, null=True, blank=True)
    # Campos de Professor
    faculty = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    # Resolve conflito do Django Auth
    groups = models.ManyToManyField('auth.Group', related_name='api_user_groups',
    blank=True)
    user_permissions = models.ManyToManyField('auth.Permission',
    related_name='api_user_permissions', blank=True)

class Project(models.Model):
    title = models.CharField(max_length=200)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    professor_name = models.CharField(max_length=200) 
    area = models.CharField(max_length=100)
    theme = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    has_scholarship = models.BooleanField(default=False)
    scholarship_details = models.CharField(max_length=200, null=True, blank=True)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    vacancies = models.IntegerField(default=1)
    description = models.TextField()
    posted_date = models.CharField(max_length=20) 
    keywords = models.CharField(max_length=255)

class Application(models.Model):
    student = models.ForeignKey(User, related_name='student_apps',
    on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    professor = models.ForeignKey(User, related_name='professor_apps',
    on_delete=models.CASCADE)
    application_date = models.CharField(max_length=20)
    motivation = models.TextField()
    status = models.CharField(max_length=50, default='Em avaliação')
    viewed_by_student = models.BooleanField(default=False)
    viewed_by_professor = models.BooleanField(default=False)