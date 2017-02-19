from django.db import models
from .patient import Patient
from .physician import Physician
from .ModelMixins import ProcedureMethods, RadiologyMethods, EchoMethods


class Radiology(RadiologyMethods, models.Model):
    MODALITIES=[
    ('XRAY','X-ray'),
    ('CT','CT'),
    ('MRI','MRI'),
    ('US','ultra-sound'),
    ]
    REGIONS=[
    ('head','Head'),
    ('brain','Brain'),
    ('neck','Neck'),
    ('heart','Heart'),
    ('chest','Chest'),
    ]

    patient=models.ForeignKey('Patient', on_delete=models.CASCADE)
    operator = models.ForeignKey('Physician',on_delete=models.PROTECT,null=True,blank=True)
    date=models.DateTimeField()
    modality=models.CharField(max_length=10, choices=MODALITIES)
    region=models.CharField(max_length=10, choices=REGIONS)
    with_contrast= models.BooleanField(default=False)
    center= models.CharField(max_length=30, null=True,blank=True)
    image = models.FileField(null=True, blank=True,)
    impression=models.TextField(null=True,blank=True)
    # document = models.FileField(upload_to='documents/{}/'.format.(patient.id))
    class Meta:
        ordering=['modality','-date',]



class Echocardiography(EchoMethods, Radiology):
    LVEDd = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    LVESd = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    SWT = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    PWT = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    EF = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    FS = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    LA = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    RV = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)
    TAPSE = models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True)

class Interventional_Radiology(ProcedureMethods, Radiology):
    pass
