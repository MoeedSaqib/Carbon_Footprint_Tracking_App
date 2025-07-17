# emissions/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Action(models.Model):
    ACTION_CHOICES = [
        ('bike', 'Used Bicycle'),
        ('plant', 'Planted a Tree'),
        ('public_transport', 'Used Public Transport'),
        ('no_plastic', 'Avoided Plastic'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    co2_saved_kg = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type} - {self.co2_saved_kg} kg"

class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'co2_saved_kg', 'date')
    list_filter = ('action_type', 'date')
    search_fields = ('user__username',)

from django.contrib.auth.models import User
from django.db import models

class TreePlanting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_trees = models.PositiveIntegerField(default=1)
    date_planted = models.DateTimeField(auto_now_add=True)

from django.db.models import Sum


class Mission(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)


from django.contrib.auth.models import User
from django.db import models

class EmissionLog(models.Model):
    CATEGORY_CHOICES = [
        ('travel', 'Travelled Responsibly'),
        ('energy', 'Saved Energy'),
        ('food', 'Ate Sustainably'),
        ('waste', 'Managed Waste'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link emission log to a user
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.FloatField()  # e.g. km, kWh, kg
    emitted = models.FloatField(default=0)  # kg CO2 actually emitted
    saved = models.FloatField(default=0)    # kg CO2 saved
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.saved} kg CO2 saved"