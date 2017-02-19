from django.db import models
from .base_models import Person
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Physician(Person):
    SPECIALITIES=[
    ('CTS','cardiothoracic surgery')
    ]

    RANKS=[
    ('HO','House Officer'),
    ('RS', 'Resident'),
    ('SP', 'Specialist'),
    ('CN', 'Consultant')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    speciality=models.CharField(max_length=6, choices=SPECIALITIES)
    rank=models.CharField(max_length=3, choices=RANKS)
    graduation_year=models.DateField(null=True,blank=True)
    def is_consultant(self):
        return self.rank =='CN'

    @receiver(post_save, sender=User)
    def create_physician(sender, instance, created, **kwargs):
        if created:
            Physician.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)

    @receiver(post_save, sender=User)
    def save_physician(sender, instance, **kwargs):
        try:
            instance.physician.first_name = instance.first_name
            instance.physician.last_name = instance.last_name
            instance.physician.email = instance.email
            instance.physician.save()
        except:
            Physician.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)
