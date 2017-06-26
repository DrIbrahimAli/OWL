from datetime import date
import pandas as pd
import re
from collections import OrderedDict

from django.db import models
from django.utils.html import format_html
from django.urls import reverse

from .utils import colorify


class PatientMethods(object):


    def get_absolute_url(self):
        return '/emr/patient/{}'.format(self.id)


    @property
    def blood_group(self):
        if self.get_abo_blood_display() and self.get_rh_blood_display():
            return '{} {}'.format(self.get_abo_blood_display(), self.get_rh_blood_display())
        else:
            return 'blood group not known'

    @property
    def never_admitted(self):
        if self.admission_set.exists():
            return False
        else:
            return True

    @property
    def last_admission(self):
        return self.admission_set.latest('pk')

    @property
    def age_on_admission(self, *args):
        try :
            admission_pk=args[0]
        except:
            admission_pk=self.last_admission.pk
        return self.admission_set.get(pk=admission_pk).date.year - self.date_of_birth.year

    @property
    def age(self):
        if self.date_of_birth:
            if self.never_admitted:
                return date.today().year - self.date_of_birth.year
            else:
                return self.age_on_admission
        else:
            return ' date of birth not known'

    @property
    def last_discharge(self):
        try:
            return self.discharge_set.latest('pk')
        except:
            return None

    @property
    def los(self):
        try:
            return str((self.last_admission.discharge.date - self.last_admission.date).days)
        except:
            return str((date.today() - self.last_admission.date).days)

    @property
    def is_currently_admitted(self):
        if not self.never_admitted:
            try:
                self.last_admission.discharge
                return False
            except:
                return True
        else:
            return False

    @property
    def has_been_discharged(self):
        if not self.never_admitted:
            return not self.is_currently_admitted
        else:
            return False

    @property
    def is_deceased(self):
        if self.never_admitted:
            return False
        elif self.is_currently_admitted:
            return False
        else:
            return self.last_discharge.mortality


    def admit(self, *args, **kwargs):
        if self.is_currently_admitted:
            print('patient is already admitted')
        else:
            print('admitting '+ str(self))
            self.admission_set.create(*args, **kwargs)

    def discharge(self,*args, **kwargs):
        if self.is_currently_admitted:
            kwargs['admission'] = kwargs.get('admission',self.last_admission)
            try:
                self.discharge_set.create(*args, **kwargs)
                print('discharging {}'.format(self))
            except Exception as e:
                print(e)
        else:
            print('{} is not admitted'.format(self))

    def get_highlights(self):
        quotes=[]
        highlights=''
        for note in self.last_admission.note_set.all():
            interest = re.compile('#.*?#').findall(note.status)
            interest += re.compile('#.*?#').findall(note.plan)
            interest += re.compile('#.*?#').findall(note.events)
            if interest:
                quotes += [[str(note.date), '\n'.join(interest).replace('#','')]]
        quotes.sort()
        for quote in quotes:
            highlights +='\n\n\t{}'.format('\n'.join(quote))
        return highlights

    def get_labs(self):
        try:
            d = OrderedDict()
            for LAB in self.patient_lab_quant_set.all():
                if LAB.lab.name not in d.keys():
                    d[LAB.lab.name] = {LAB.time.strftime('%Y/%m/%d</br>%H.%M') : LAB.result_with_alert()}
                else:
                    d[LAB.lab.name].update({LAB.time.strftime('%Y/%m/%d</br>%H.%M'):LAB.result_with_alert()})
            df=pd.DataFrame(d)
            df.sort_index(inplace=True, ascending=False)
            pd.set_option('display.max_colwidth',-1)
            return format_html(df.to_html(
                        classes='table table-responsive table-striped table-bordered table-condensed',
                        na_rep='',
                        justify='center',
                        escape=False))
        except:
            pass

    def get_risk(self):
        history = self.history
        risk='A '
        if history.is_hypertensive:
            risk += 'hypertensive '
        if history.is_diabetic_I:
            risk += 'diabetic, type II; '
        if history.is_diabetic_II:
            risk += 'diabetic, type I; '
        if history.is_dyslipidemic:
            risk += 'dyslipidemic; '
        if history.is_smoker:
            risk += 'smoker '
        risk += self.age + self.get_sex_display() + ' patient.'
        return risk

    def get_present_history(self):
        return self.history.present_history

    def get_past_history(self):
        return self.history.past_history

    def get_allergies(self):
        return self.history.drug_and_allergy

    def get_history(self):
        return '''
{}
{}
{}
{}
        '''.format(self.get_risk(), self.history.present_history, self.history.past_history, self.history.drug_and_allergy)

class PatientUrlMixin(object):
    def get_absolute_url(self):
        return '/emr/patient/{}'.format(self.patient.id)

class TransferMethods(PatientUrlMixin):
    pass

class NoteMethods(PatientUrlMixin):

    def colored(self):
        return format_html(colorify('''
        <span class="text-info">status</span>
        {}

        <span class="text-info">plan</span>
        {}

        <span class="text-info">events</span>
        {}
        '''.format(self.status, self.plan, self.events)))


class ProcedureMethods(PatientUrlMixin, models.Model):

    name = models.CharField(max_length=100)
    anaesthelogist = models.ForeignKey('Physician',
        on_delete=models.PROTECT,
        related_name='anaesthetizing_for',
        null=True, blank=True)
    details = models.TextField()
    complications = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return '{} on {}'.format(self.name, str(self.date))

    class Meta:
        abstract = True


class LabMethods(PatientUrlMixin):

    class Meta:
        ordering = ['pk']


class LabQuantMethods(LabMethods):

    def result_with_alert(self):
        result = self.result
        value = str(result)
        max_threshold = max(self.lab.limit_max, self.lab.accepted_max)
        min_threshold = min(self.lab.limit_min, self.lab.accepted_min)
        if (result <= self.lab.limit_max) and (result >= self.lab.limit_min):
            value = colorify(value,pattern='(?P<colored>.*)',ALERT='primary',url='/emr/lab_quant/{}'.format(self.pk))
        elif (result > max_threshold) or (result < min_threshold):
            value = colorify(value,pattern='(?P<colored>.*)',ALERT='warning',url='/emr/lab_quant/{}'.format(self.pk))
        else:
            value = colorify(value,pattern='(?P<colored>.*)',ALERT='success',url='/emr/lab_quant/{}'.format(self.pk))
        return format_html(value)


class RadiologyMethods(PatientUrlMixin):

    def __str__(self):
        if self.with_contrast:
            contrast = 'with contrast'
        else: contrast = ''
        if self.modality == 'US' and self.region =='heart':
            name = 'Echocardiography'
        elif self.modality == 'FLURO' and self.region =='vas':
            name = 'Angiography'
        elif self.modality == 'FLURO' and self.region =='coronary':
            name = 'Coronary Angiography'
        else:
            name = '{} {}'.format(self.get_region_display(), self.get_modality_display())
        return '{} {} on {}'.format(name, contrast, str(self.date.strftime('%Y/%m/%d')))

    def report(self):
        if self.operator:
            operator = 'by {}'.format(self.operator)
        else:
            operator=''
        report = '''
        {}
        {}

        {}
        '''.format(self, operator, self.impression)
        return format_html(report)


class EchoMethods(RadiologyMethods):

    def __str__(self):
        return 'Echocardiography on {}'.format(str(self.date.strftime('%Y/%m/%d')))

    def report(self):
        if self.operator:
            operator = 'by {}'.format(self.operator)
        else:
            operator=''
        report = '''
        {}
        {}

        <div class="table-responsive">\
          <table class="table table-striped" style="text-align : center">\
            <tbody>\
              <tr>\
                <td>LVED</td><td>{}</td><td>LA</td><td>{}</td><td>RV</td><td>{}</td>\
              </tr>\
              <tr>\
                <td>LVES</td><td>{}</td><td></td><td></td><td>TAPSE</td><td>{}</td>\
              </tr>\
              <tr>\
                <td>SWT</td><td>{}</td><td>EF</td><td>{}</td><td></td>\
              </tr>\
              <tr>\
                <td>PWT</td><td>{}</td><td>FS</td><td>{}</td><td></td>\
              </tr>\
            </tbody>\
          </table>\
        </div>

        {}
        '''.format(
             self, operator, self.LVEDd,
             self.LA, self.RV, self.LVESd,
             self.TAPSE, self.SWT, self.EF,
             self.PWT, self.FS, self.impression
        )
        return format_html(report)
