from django.db import models
from datetime import date
from django.utils import timezone
from pycountry import countries
from .ModelMixins import LabMethods, TransferMethods
from .utils import normalising_map, normalizeArabic

class Person(models.Model):
    Country= list(countries)
    NATIONALITIES=[]
    for i in range(len(Country)):
        NATIONALITIES.append((Country[i].alpha_3,Country[i].name))
    SEX_CHOICES = [
        ('M', 'male'),
        ('F', 'female')]

    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=90,blank=True)
    last_name = models.CharField(max_length=30)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    id_card = models.PositiveIntegerField(null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    nationality = models.CharField(max_length=3, choices=NATIONALITIES, default='EGY')
    phone = models.CharField(max_length=20, null=True,blank=True)
    address = models.CharField(max_length=300, null=True,blank=True)
    email = models.EmailField(null =True,blank=True)


    def __str__(self):
        return  '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)

    def save(self):
        self.first_name = normalizeArabic(self.first_name)
        self.middle_name = normalizeArabic(self.middle_name)
        self.last_name = normalizeArabic(self.last_name)
        super().save()


    class Meta:
        abstract = True



class Transfer(TransferMethods, models.Model):
    LOCATIONS = [
    ('OR','Operating Room'),
    ('ED','Emergency Department'),
    ('WRD','in-patient ward'),
    ('OTHR','another center/hospital'),
    ('ICU1','ICU-1'),
    ('ICU2','ICU-2'),
    ('ICU3','ICU-3'),
    ('ICU4','ICU-4'),
    ('MORT','Mortuary'),
    ]
    date=models.DateField(default=date.today)
    patient=models.ForeignKey('Patient', on_delete=models.CASCADE)
    transfer_to = models.CharField(max_length=4, choices=LOCATIONS)
    transfer_from = models.CharField(max_length=4, choices=LOCATIONS)
    status_on_transfer = models.TextField()

    def __str__(self):
        return '{0} transferred on {3} from {1} to {2}'.format(self.patient, self.transfer_from, self.transfer_to, self.date)

    class Meta:
        abstract = True
        ordering = ['-id']
        get_latest_by = ['-id']


class Lab(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    class Meta:
        abstract=True


class Patient_Lab(LabMethods, models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str()

    class Meta:
        abstract=True



# class Document(models.Model):
#     patient=models.ForeignKey('Patient', on_delete=models.CASCADE)
#     description = models.CharField(max_length=255, null=True,blank=True)
#     document = models.FileField(upload_to='documents/{}/'.format(patient))
