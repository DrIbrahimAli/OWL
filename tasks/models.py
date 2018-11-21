from django.db import models
from django.urls import reverse
from datetime import date
from emr.models.patient import Patient

class Task(models.Model):
    PRIORITY_LEVELS=[
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ]
    due_date = models.DateField(default=date.today)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        # limit_choices_to=list(Patient.objects.current()),
        null=True, blank=True,
        )
    description = models.CharField(max_length=300)
    priority = models.CharField(max_length=1, default='1', choices=PRIORITY_LEVELS)
    comments = models.CharField(max_length=300, null=True, blank=True)
    done = models.BooleanField(default=False)

    def get_absolute_url(self):
        return '/tasks/list/undone'

    class Meta:
        ordering = ['due_date', 'patient', 'priority',]
