from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from ckeditor.widgets import CKEditorWidget
from .models.patient import *
from .models.physician import *
from .models.labs import *
from .models.procedure import *
from .models.radiology import *



class PhysicianForm(forms.ModelForm):
    class Meta:
        model = Physician
        exclude = ('user',)
        widgets = {
        'date_of_birth': AdminDateWidget
        }



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields= '__all__'
        widgets = {
        'date_of_birth': AdminDateWidget
        }

class PatientThingFormMixin(forms.ModelForm):
    class Meta:
        exclude = ('patient',)


class HistoryForm(PatientThingFormMixin):
    class Meta:
        model = History
        exclude = ('patient',)

class AdmissionForm(PatientThingFormMixin):
    class Meta:
        model = Admission
        exclude = ('patient',)
        widgets = {
        'date': AdminDateWidget
        }

class DischargeForm(PatientThingFormMixin):
    class Meta:
        model = Discharge
        exclude = ('patient','admission', 'transfer_from')
        widgets = {
        'date': AdminDateWidget
        }

    def clean(self):
        super().clean()
        status = self.cleaned_data.get('status_on_transfer')
        mortality = self.cleaned_data.get('mortality')
        recommendations = self.cleaned_data.get('recommendations')
        print(self.cleaned_data)
        if mortality:
            self.cleaned_data.update(
                status_on_transfer = 'Deceased',
                recommendations = '',
                transfer_to = 'MORT'
            )
        elif not mortality and (len(recommendations) < 30):
            # raise ValidationError('are you sure those are all the recommendations!')
            self.add_error('recommendations', 'are you sure those are all the recommendations')

class NoteForm(PatientThingFormMixin):
    class Meta:
        model = Note
        exclude = ('patient','admission', 'physician')
        widgets = {
        'date': AdminDateWidget,
        }


class RadiologyForm(PatientThingFormMixin):
    class Meta:
        model = Radiology
        exclude = ('patient',)
        widgets = {
        'date': AdminDateWidget
        }


class EchocardiographyForm(PatientThingFormMixin):
    class Meta:
        model = Echocardiography
        exclude = ('patient','modality', 'region', 'with_contrast')
        widgets = {
        'date': AdminDateWidget
        }


class Interventional_RadiologyForm(PatientThingFormMixin):
    class Meta:
        model = Interventional_Radiology
        # exclude = ('patient',)
        fields = [
            'date',
            'center',
            'modality',
            'region',
            'with_contrast',
            'operator',
            'anaesthelogist',
            'name',
            'details',
            'impression',
        ]
        widgets = {
        'date': AdminDateWidget
        }


class ProcedureForm(PatientThingFormMixin):
    class Meta:
        model = Procedure
        exclude = ('patient',)
        widgets = {
        'date': AdminDateWidget
        }


class SurgeryForm(PatientThingFormMixin):
    class Meta:
        model = Surgery
        exclude = ('patient',)
        widgets = {
        'date': AdminDateWidget
        }


class Lab_QualForm(PatientThingFormMixin):
    class Meta:
        model = Patient_Lab_qual
        exclude = ('patient',)


class Lab_QuantForm(PatientThingFormMixin):
    class Meta:
        model = Patient_Lab_quant
        exclude = ('patient',)



class CultureForm(PatientThingFormMixin):
    class Meta:
        model = Culture
        exclude = ('patient',)
        widgets = {
        'date': AdminDateWidget
        }


class Fluid_analysisForm(PatientThingFormMixin):
    class Meta:
        model = Fluid_analysis
        exclude = ('patient',)
        widgets = {
        'date': AdminDateWidget
        }


class RoutineLabForm(forms.Form):

    time = forms.DateTimeField(widget=AdminSplitDateTime)

    urea = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    # BUN = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    creat = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    AST = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    ALT = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Bil_total = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Bil_direct = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    GGT = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    ALP = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Alb = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    ptn = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Trop_I = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    CK = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    CKmb = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    # LDH = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    # amylase = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    # lipase = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    # CRP = forms.DecimalField(max_digits=7, decimal_places=2,required=False)

    Hb = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    TLC  = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    plt  = forms.DecimalField(max_digits=7, decimal_places=2,required=False)

    PT = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    PC = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    INR = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    PTT = forms.DecimalField(max_digits=7, decimal_places=2,required=False)

    Na = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    K = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    phos = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Ca_ionized = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Ca_total = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
    Mg = forms.DecimalField(max_digits=7, decimal_places=2,required=False)
