from django.db import models
# from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    STATUS_CHOICES = (("m","management"),("t","teacher"),("s","student"))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="s",blank = True,null = True)
    national_code = models.CharField(max_length = 10,unique = True)
    bio = models.TextField(blank=True, null=True)
    # location = gis_models.PointField(srid=4326, null=True, blank=True)
 
    def __str__(self):
        return F"{self.username} --- {self.first_name} {self.last_name}"
    
    
class QueueSignUp(models.Model):
    STATUS_CHOICES = (("p","Pending"),("a","Accepted"),("r","Rejected"))
    ROLE_CHOICES = (("t","teacher"),("s","student"))
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    national_code = models.CharField(max_length = 10)#,unique = True
    email = models.EmailField()#,unique = True
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p")
    rejection_reason = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default="s")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return F"{'student' if self.role == 's' else 'teacher' } --- {self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ('-updated_at',)