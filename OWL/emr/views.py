from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models.patient import *
from .models.labs import *
from .models.procedure import *
from .models.radiology import *
from .forms import *


class PatientThingViewMixin(LoginRequiredMixin):
    template_name= 'emr/patient_related_form.html'


class PatientThingCreateMixin(PatientThingViewMixin):

    # def auto_assign(self,request, *args, **kwargs):
    #     form = self.get_form()


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            patient_thing=form.save(commit=False)
            patient_thing.patient=Patient.objects.get(pk=kwargs['patient_id'])
            patient_thing.save()
            return HttpResponseRedirect(patient_thing.get_absolute_url())
        else:
            return self.form_invalid(form)

class Home(LoginRequiredMixin, generic.ListView):
    template_name = 'emr/home.html'
    context_object_name = 'current_patients'
    def get_queryset(self):
        IDs = [p.pk for p in Patient.objects.all() if p.is_currently_admitted()]
        return Patient.objects.filter(pk__in=IDs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Home, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['Patient'] = Patient.objects
        return context


class PhysicianAdd(LoginRequiredMixin, generic.CreateView):
    model = Physician
    form_class= PhysicianForm
    template_name='emr/patient_related_form.html'


class PhysicianEdit(LoginRequiredMixin, generic.UpdateView):
    model = Physician
    form_class= PhysicianForm
    template_name='emr/patient_related_form.html'


@login_required
def patient_detail(request, pk):

    context={}
    context['patient'] = Patient.objects.get(pk=pk)
    return render(request, 'emr/patient_detail.html', context )


class PatientAdd(LoginRequiredMixin, generic.CreateView):
    model = Patient
    form_class= PatientForm
    template_name='emr/patient_related_form.html'


class PatientEdit(LoginRequiredMixin, generic.UpdateView):
    model = Patient
    form_class= PatientForm
    template_name= 'emr/patient_related_form.html'


class HistoryAdd(PatientThingCreateMixin, generic.CreateView):
    model = History
    form_class= HistoryForm


class HistoryEdit(PatientThingViewMixin, generic.UpdateView):
    model = History
    form_class= HistoryForm


class PatientAdmit(PatientThingCreateMixin, generic.CreateView):
    model = Admission
    form_class = AdmissionForm


class AdmissionEdit(PatientThingViewMixin, generic.UpdateView):
    model = Admission
    form_class = AdmissionForm


class PatientDischarge(PatientThingCreateMixin, generic.CreateView):
    model = Discharge
    form_class= DischargeForm
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            patient_thing=form.save(commit=False)
            patient_thing.patient=Patient.objects.get(pk=kwargs['patient_id'])
            patient_thing.admission= patient_thing.patient.last_admission()
            patient_thing.transfer_from= patient_thing.patient.last_admission().transfer_to
            patient_thing.save()
            return HttpResponseRedirect(patient_thing.get_absolute_url())
        else:
            return self.form_invalid(form)


class DischargeEdit(PatientThingViewMixin, generic.UpdateView):
    model = Discharge
    form_class= DischargeForm


class NoteAdd(PatientThingCreateMixin, generic.CreateView):
    model = Note
    form_class= NoteForm

    # def auto_assign(self,request, *args, **kwargs):
    #     form = self.get_form()
    #     patient_thing=form.save(commit=False)
    #     patient_thing.patient=Patient.objects.get(pk=kwargs['patient_id'])
    #     patient_thing.save()
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            patient_thing = form.save(commit=False)
            patient_thing.patient = Patient.objects.get(pk=kwargs['patient_id'])
            patient_thing.admission = patient_thing.patient.last_admission()
            patient_thing.physician = request.user.physician
            patient_thing.save()
            return HttpResponseRedirect(patient_thing.get_absolute_url())
        else:
            return self.form_invalid(form)


class NoteEdit(PatientThingViewMixin, generic.UpdateView):
    model = Note
    form_class= NoteForm


class RadiologyAdd(PatientThingCreateMixin, generic.CreateView):
    model = Radiology
    form_class= RadiologyForm


class RadiologyEdit(PatientThingViewMixin, generic.UpdateView):
    model = Radiology
    form_class= RadiologyForm


class EchocardiographyAdd(PatientThingCreateMixin, generic.CreateView):
    model = Echocardiography
    form_class= EchocardiographyForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            patient_thing=form.save(commit=False)
            patient_thing.patient=Patient.objects.get(pk=kwargs['patient_id'])
            patient_thing.modality= 'US'
            patient_thing.region= 'heart'
            patient_thing.with_contrast= False
            patient_thing.save()
            return HttpResponseRedirect(patient_thing.get_absolute_url())
        else:
            return self.form_invalid(form)


class EchocardiographyEdit(PatientThingViewMixin, generic.UpdateView):
    model = Echocardiography
    form_class= EchocardiographyForm


class Interventional_RadiologyAdd(PatientThingCreateMixin, generic.CreateView):
    model = Interventional_Radiology
    form_class= Interventional_RadiologyForm


class Interventional_RadiologyEdit(PatientThingViewMixin, generic.UpdateView):
    model = Interventional_Radiology
    form_class= Interventional_RadiologyForm


class Lab_QualAdd(PatientThingCreateMixin, generic.CreateView):
    model = Patient_Lab_qual
    form_class= Lab_QualForm


class Lab_QualEdit(PatientThingViewMixin, generic.UpdateView):
    model = Patient_Lab_qual
    form_class= Lab_QualForm


class Lab_QuantAdd(PatientThingCreateMixin, generic.CreateView):
    model = Patient_Lab_quant
    form_class= Lab_QuantForm


class Lab_QuantEdit(PatientThingViewMixin, generic.UpdateView):
    model = Patient_Lab_quant
    form_class= Lab_QuantForm



class CultureAdd(PatientThingCreateMixin, generic.CreateView):
    model = Culture
    form_class= CultureForm


class CultureEdit(PatientThingViewMixin, generic.UpdateView):
    model = Culture
    form_class= CultureForm


class Fluid_analysisAdd(PatientThingCreateMixin, generic.CreateView):
    model = Fluid_analysis
    form_class= Fluid_analysisForm


class Fluid_analysisEdit(PatientThingViewMixin, generic.UpdateView):
    model = Fluid_analysis
    form_class= Fluid_analysisForm


@login_required
def routine_lab(request, patient_id):

    patient = Patient.objects.get(pk=patient_id)

    if request.method == 'POST':
        form = RoutineLabForm(request.POST)
        print(form)
        if form.is_valid():
            print(form.cleaned_data)
            time = form.cleaned_data.get('time')
            for lab in form.cleaned_data.keys():
                if not lab == 'time':
                    try:
                        Patient_Lab_quant(
                            result=form.cleaned_data.get(lab),
                            lab=Lab_quant.objects.get(name=lab),
                            time=time,
                            patient=patient
                            ).save()
                        print('done')
                    except:
                        print('naa')
            return HttpResponseRedirect(patient.get_absolute_url())

    else:
        form = RoutineLabForm()

    return render(request, 'emr/patient_related_form.html', {'form':form} )


class ProcedureAdd(PatientThingCreateMixin, generic.CreateView):
    model = Procedure
    form_class= ProcedureForm


class ProcedureEdit(PatientThingViewMixin, generic.UpdateView):
    model = Procedure
    form_class= ProcedureForm


class SurgeryAdd(PatientThingCreateMixin, generic.CreateView):
    model = Surgery
    form_class= SurgeryForm


class SurgeryEdit(PatientThingViewMixin, generic.UpdateView):
    model = Surgery
    form_class= SurgeryForm
