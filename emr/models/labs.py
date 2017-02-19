from django.db import models
from .base_models import Lab, Patient_Lab
from .patient import Patient
from .ModelMixins import LabQuantMethods


class Lab_quant(Lab):
    unit = models.CharField(max_length=10,blank=True)
    limit_max = models.DecimalField(max_digits=7, decimal_places=2)
    limit_min = models.DecimalField(max_digits=7, decimal_places=2)
    accepted_max = models.DecimalField(max_digits=7, decimal_places=2)
    accepted_min = models.DecimalField(max_digits=7, decimal_places=2)

class Lab_qual(Lab):
    pass

class Patient_Lab_qual(Patient_Lab):
    RESULTS=[
        ('P','+ve'),
        ('N','-ve')]

    lab= models.ForeignKey('Lab_qual')
    result=models.CharField(max_length=1, choices=RESULTS)

class Patient_Lab_quant(LabQuantMethods, Patient_Lab):
    lab = models.ForeignKey('Lab_quant')
    result = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return '{} {} ===> {}'.format(str(self.time), self.lab.name, str(self.result))

    class Meta:
        ordering=['lab']

class Culture(Patient_Lab):
    date_of_result = models.DateField(null=True, blank=True)
    specimen = models.CharField(max_length=50)
    direct_film = models.CharField(max_length=300, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)
    organisms = models.CharField(max_length=300, null=True, blank=True)
    sensitive_to = models.TextField(null=True, blank=True)
    resistant_to = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.specimen) + ' culture'

    def results_retrieved(self):
        if self.date_of_result:
            return True
        else:
            return False

class Fluid_analysis(Patient_Lab):
    specimen = models.CharField(max_length=50)
    report = models.TextField()
