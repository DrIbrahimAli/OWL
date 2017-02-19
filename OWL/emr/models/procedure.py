from django.db import models
from .patient import Patient
from .physician import Physician
from .ModelMixins import ProcedureMethods


class Procedure(ProcedureMethods, models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    operator = models.ForeignKey('Physician',on_delete=models.PROTECT, related_name='operating_on')
    date = models.DateField()


class Surgery(Procedure):
    pass
