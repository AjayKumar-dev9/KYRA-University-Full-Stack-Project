from django.db import models

# Create your models here.

class student_record(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    GRADUATION_STATUS = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ph_no = models.CharField(max_length=12)
    email = models.EmailField()
    dob = models.DateField()
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    graduation_completed = models.CharField(max_length=3,choices=GRADUATION_STATUS)
    course = models.CharField(max_length=50)
    image = models.ImageField(upload_to="image/")

    def __str__(self):
        return self.first_name


    class meta:
        verbose_name = 'record'
        verbose_name_plural  = 'records'
