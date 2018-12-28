from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

# Create your models here.

class User(models.Model):
    telegram_id = models.CharField(max_length=20, unique=True)
    mode = models.CharField(max_length=100, blank=True)
    temp_data = models.CharField(max_length=90000, blank=True)
    queue = models.CharField(max_length=10000, blank=True)
    levels = models.CharField(max_length=100, blank=True)
    time_to_ask = models.DateTimeField(default=datetime(2019,1,1,7,0,0,0))

    def __str__(self):
        return self.telegram_id


class Leitner_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    q = models.CharField(max_length=90000)
    a = models.CharField(max_length=90000)
    level = models.IntegerField(default=1, validators=[
        MaxValueValidator(5),
        MinValueValidator(1),
    ])
    date_of_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.q


class MessageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    metadata = models.TextField(max_length=90000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Setting(models.Model):
    priority = models.IntegerField(unique=True)
    telegram_welcome_text = models.TextField(max_length=4000)
    telegram_start_text = models.TextField(max_length=1000)
    start_date = models.DateTimeField(auto_now=True)
    enter_answer_text = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.priority)
