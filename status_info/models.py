import os
from django.db import models
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User


class Title(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=520)
    description = models.TextField(max_length=5110)

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=520)
    description = models.TextField(max_length=5110)
    current = models.BooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.current:
            return super(Job, self).save(*args, **kwargs)
        with transaction.atomic():
            Job.objects.filter(user=self.user, current=True).update(current=False)
            return super(Job, self).save(*args, **kwargs)


class Skill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=520)
    description = models.TextField(max_length=5110)
    active = models.BooleanField()
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Language(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=128)
    comprehension = models.FloatField()

    def __str__(self):
        return self.name


class UserStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    backend_stat = models.IntegerField(default=0)
    frontend_stat = models.IntegerField(default=0)
    data_science_stat = models.IntegerField(default=0)
    data_base_stat = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Quest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    date = models.DateTimeField('date published', auto_now_add=True)
    description = models.TextField(max_length=5110)
    completed = models.BooleanField()

    def __str__(self):
        return self.name


class Reflection(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=256)
    date = models.DateTimeField('date published', auto_now_add=True)
    description = models.TextField(max_length=5110)
    gains = models.TextField(max_length=5110)

    def __str__(self):
        return self.title



