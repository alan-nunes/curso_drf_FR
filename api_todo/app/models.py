from django.db import models

class Todo(models.Model):
    name = models.CharField(max_length=120)
    done = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True) #add automaticamente a data
    