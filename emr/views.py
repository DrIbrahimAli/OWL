import operator
from functools import reduce

from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.http.response import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models.patient import *
from .models.labs import *
from .models.procedure import *
from .models.radiology import *
from .models.utils import is_int
from .forms import *


class PatientThingViewMixin(LoginRequiredMixin):
    template_name= 'emr/patient_related_form.html'


class PatientThingCreateMixin(PatientThingViewMixin):


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs['patient_id'])
        self.object.save()
        return super().form_valid(form)


class Home(LoginRequiredMixin, generic.ListView):
    template_name = 'emr/home.html'
    context_object_name = 'current_patients'
    def get_queryset(self):
        return Patient.objects.current()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Home, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['Patient'] = Patient.objects
        return context


class PatientSearch(LoginRequiredMixin, generic.ListView):
    model = Patient
    template_name = 'emr/search_results.html'
#    paginate_by = 10

    def get_queryset(self):


        result = super().get_queryset()

        query = self.request.GET.get('q')
        query_list = [i for i in query.split() if not is_int(i)]
        num_list = [i for i in query.split() if is_int(i)]
        if query_list:
            result = result.filter(
                reduce(operator.or_,
                       (Q(first_name__icontains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(middle_name__icontains=q) for q in query_list)) |
                reduce(operator.or_,
                       (Q(last_name__icontains=q) for q in query_list))
            )
        if num_list:
            result = result.filter(
                reduce(operator.or_,
                       (Q(serial_no=q) for q in num_list))
           )
        return result


class PhysicianAdd(LoginRequiredMixin, generic.CreateView):
    model = Physician
    form_class= PhysicianForm
    template_name='emr/patient_related_form.html'
    success_url = '/emr'


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

    def get_success_url(self):
        return reverse('emr:patient_admit',args=(self.object.id,))

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

    def get_success_url(self):
        admission = self.object
        print(self.object)
        patient = admission.patient
        try:
            history = patient.history
            return reverse('emr:history_edit',args=(history.pk,))
        except:
            return reverse('emr:history_add',args=(patient.pk,))


class AdmissionEdit(PatientThingViewMixin, generic.UpdateView):
    model = Admission
    form_class = AdmissionForm


class PatientDischarge(PatientThingCreateMixin, generic.CreateView):
    model = Discharge
    form_class= DischargeForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs['patient_id'])
        self.object.admission= self.object.patient.last_admission()
        self.object.transfer_from= self.object.patient.last_admission().transfer_to
        self.object.save()
        return super().form_valid(form)


class DischargeEdit(PatientThingViewMixin, generic.UpdateView):
    model = Discharge
    form_class= DischargeForm

@login_required
def dischargeSummary(request, pk):
    discharge = Discharge.objects.get(pk=pk)
    patient = discharge.patient
    admission = discharge.admission
    context = {
        'discharge':discharge,
        'patient':patient,
        'admission':admission
    }
    # context['string'] = 'just a test string'
    response = HttpResponse(content_type="text/plain; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename="discharge"'
    t = loader.get_template('emr/discharge')
    c = Context(context)
    response.write(t.render(c))
    return response



class NoteAdd(PatientThingCreateMixin, generic.CreateView):
    model = Note
    form_class= NoteForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs['patient_id'])
        self.object.admission = self.object.patient.last_admission()
        self.object.physician = self.request.user.physician
        self.object.save()
        return super().form_valid(form)


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

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.patient=Patient.objects.get(pk=self.kwargs['patient_id'])
        self.object.modality= 'US'
        self.object.region= 'heart'
        self.object.with_contrast= False
        self.object.save()
        return super().form_valid(form)


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
                    except:
                        pass
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
