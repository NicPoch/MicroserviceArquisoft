from django.db import models

# Create your models here.
class AuthUser(models.Model):
    choices=[("BOOKLICK_ADMIN","Booklick Administrator"),("UNIVERSITY_ADMIN","University Administrator"),("STUDENT","Student"),("PROFESOR","profesor"),("USER","user")]
    password=models.TextField(blank=False,null=False,default=None)
    username=models.TextField(blank=False,null=False,default=None,unique=True)
    rol=models.TextField(blank=False,null=False,default=None,choices=choices)
    def __str__(self):
        return "User "+str(self.pk)+"---"+self.rol