from django.db import models
from datetime import date
from django.utils import timezone
from .base_models import Person, Transfer
from .ModelMixins import PatientMethods, NoteMethods, PatientUrlMixin


class PatientManager(models.Manager):

    def current(self):
        IDs = [p.pk for p in self.objects.all() if p.is_currently_admitted()]
        return self.objects.filter(pk__in=IDs)

    def month_admissions(self):
        return Admission.objects.filter(
            date__month=date.today().month,
            date__year = date.today().year,
            ).count()

    def month_mortality(self):
        return Discharge.objects.filter(
            date__month=date.today().month,
            date__year = date.today().year,
            mortality = True
            ).count()


class Patient(PatientMethods, Person):
    ABO=[
        ('A','A'),
        ('B','B'),
        ('O','O')]
    RH=[
        ('P','+ve'),
        ('N','-ve')]
    serial_no = models.PositiveIntegerField(unique=True)
    weight = models.PositiveIntegerField(null=True,blank=True)
    height = models.PositiveIntegerField(null=True,blank=True)
    abo_blood=models.CharField(max_length=1, choices=ABO,null=True,blank=True)
    rh_blood=models.CharField(max_length=1, choices=RH,null=True,blank=True)
    objects= PatientManager()


class History(PatientUrlMixin, models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    is_hypertensive= models.BooleanField(default=False)
    is_smoker= models.BooleanField(default=False)
    is_dyslipidemic= models.BooleanField(default=False)
    is_diabetic_I= models.BooleanField(default=False)
    is_diabetic_II= models.BooleanField(default=False)
    present_history = models.TextField(null=True, blank=True)
    past_history = models.TextField(null=True, blank=True)
    drug_and_allergy = models.TextField(null=True, blank=True)


class Admission(Transfer):
    SCORES=[
    ('APACHE_II','APACHE_II'),
    ('EUROSCORE_II','EUROSCORE_II')
    ]
    consultant = models.ManyToManyField('Physician', limit_choices_to={'rank':'CN'})
    score_system = models.CharField(max_length=12,choices=SCORES)
    risk_score = models.PositiveSmallIntegerField(null=True,blank=True)
    cause_of_admission = models.CharField(max_length=300)


class Discharge(Transfer):
    admission = models.OneToOneField('Admission')
    mortality = models.BooleanField(default=False)
    recommendations = models.TextField()

class Note(NoteMethods, models.Model):
    date=models.DateField(default=date.today)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    admission = models.ForeignKey('Admission', on_delete=models.CASCADE)
    physician = models.ForeignKey('Physician', on_delete=models.PROTECT)
    sofa_score = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.TextField()
    plan = models.TextField()
    events = models.TextField()

    class Meta:
        ordering=['-date','-admission']
