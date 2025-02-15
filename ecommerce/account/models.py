from django.db import models
from django.contrib.auth.models import User


class UserEmails(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, blank=False)
    verified = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now=True)
    registration_verification = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "email history"

    def __str__(self):
        return f"{self.user} ({self.email})"
    

class PasswordResetEmails(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, blank=False)
    reset = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "password history"

    def __str__(self):
        return f"{self.user} ({self.email})"
