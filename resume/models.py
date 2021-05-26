from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Resume(models.Model):
    description = models.CharField(max_length=1024)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.description
