from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Course(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    address = models.TextField(max_length=500)
    website = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Member(models.Model):

    name = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    email = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="members")

    def __str__(self):
        return self.name


class Club(models.Model):
    title= models.CharField(max_length = 150)
    members = models.ManyToManyField(Member)
    def __str__(self):
        return self.title



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     favorite_color = models.CharField(max_length=50)
# will add Profile feature later
