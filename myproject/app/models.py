from django.db import models

class UserModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20, null=False)

