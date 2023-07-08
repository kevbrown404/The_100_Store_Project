from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Designer(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=250)
    bio = models.TextField(max_length=500)
    verified_designer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Item(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.title
