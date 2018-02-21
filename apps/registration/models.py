from django.db import models

from django.contrib.auth.models import AbstractUser


class Application(models.Model):
    STATUS_PREPARING = "preparing"
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_PREPARING, "Preparing"),
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    )

    name = models.CharField(max_length=128)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)

    def __str__(self):
        return "{} ({})".format(self.name, self.hackathon)


class Applicant(AbstractUser):
    github_user_name = models.CharField(max_length=39, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=200, help_text='Required', unique=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_username(self):
        return self.email
