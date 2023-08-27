from django.db import models
from django.contrib.auth.models import AbstractUser

# The below contains the choices for user_type.
USER_TYPE_CHOICES=(
        ("volunteer",'volunteer'),
        ("organisation",'organisation'),
        ) #the form of these choices lists is ([value],[label]),

#The model inherits from Django's AbstractUser which already has the username and password fields.
class CustomUser(AbstractUser):
    user_type=models.CharField(max_length=25, choices = USER_TYPE_CHOICES)


