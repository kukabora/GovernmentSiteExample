from django.db import models


class Citizen(models.Model):
    first_name = models.CharField(name="first_name", max_length=100)
    email = models.CharField(name="email", max_length=100)
    password = models.CharField(name="password", max_length=100)
    department = models.CharField(max_length=100)
    avatar = models.ImageField(name="avatar", upload_to='avatars')
    amount_of_accepted_projects = models.IntegerField(default=0)
    last_name = models.CharField(name="last_name", max_length=100, default="")
    bday = models.DateField(name="birth_day", auto_now=False)
    gender = models.CharField(name="gender", default="Other", max_length=15)
    age = models.IntegerField(name="age", default=0)

    class Meta:
        verbose_name = 'Citizen'
        verbose_name_plural = 'Citizens'




# Create your models here.