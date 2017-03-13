from django.db import models
from datetime import date
from django.utils import timezone
from .base_models import Person, Transfer
from .ModelMixins import PatientMethods, NoteMethods, PatientUrlMixin


class PatientManager(models.Manager):

    def current(self):
        IDs = [p.pk for p in self.all() if p.is_currently_admitted()]
        return self.filter(pk__in=IDs)

    def month_admissions(self):
        return self.filter(
            admission__date__month=date.today().month,
            admission__date__year = date.today().year,
            )

    def month_mortality(self):
        return self.filter(
            discharge__date__month=date.today().month,
            discharge__date__year = date.today().year,
            discharge__mortality = True
            )


class Patient(PatientMethods, Person):
    ABO=[
        ('AB','AB'),
        ('A','A'),
        ('B','B'),
        ('O','O')]
    RH=[
        ('P','+ve'),
        ('N','-ve')]
    serial_no = models.PositiveIntegerField(unique=True)
    weight = models.PositiveIntegerField(null=True,blank=True)
    height = models.PositiveIntegerField(null=True,blank=True)
    abo_blood=models.CharField(max_length=2, choices=ABO,null=True,blank=True)
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
    risk_score = models.DecimalField(max_digits=7,decimal_places=2)
    cause_of_admission = models.CharField(max_length=300)


class Discharge(Transfer):
    admission = models.OneToOneField('Admission')
    mortality = models.BooleanField(default=False)
    recommendations = models.TextField(blank=True)

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
