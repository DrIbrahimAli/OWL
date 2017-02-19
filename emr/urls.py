from django.conf.urls import url, include
from . import views

app_name='emr'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),

    url(r'^physician/add$', views.PhysicianAdd.as_view(), name='physician_add'),
    url(r'^physician/(?P<pk>[0-9]+)/edit$', views.PhysicianEdit.as_view(), name='physician_edit'),

    url(r'^patient/search$', views.PatientSearch.as_view(), name='patient_search'),

    url(r'^patient/add$', views.PatientAdd.as_view(), name='patient_add'),
    url(r'^patient/(?P<pk>[0-9]+)/$', views.patient_detail, name='patient_detail'),
    url(r'^patient/(?P<pk>[0-9]+)/edit$', views.PatientEdit.as_view(), name='patient_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/admit$', views.PatientAdmit.as_view(), name='patient_admit'),
    url(r'^patient/(?P<patient_id>[0-9]+)/admission/(?P<pk>[0-9]+)$', views.AdmissionEdit.as_view(), name='admission_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/discharge$', views.PatientDischarge.as_view(), name='patient_discharge'),
    url(r'^patient/(?P<patient_id>[0-9]+)/discharge/(?P<pk>[0-9]+)$', views.DischargeEdit.as_view(), name='discharge_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/history$', views.HistoryAdd.as_view(), name='history_add'),
    url(r'^patient/[0-9]+/history/(?P<pk>[0-9]+)$', views.HistoryEdit.as_view(), name='history_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/note$', views.NoteAdd.as_view(), name='note_add'),
    url(r'^patient/[0-9]+/note/(?P<pk>[0-9]+)$', views.NoteEdit.as_view(), name='note_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/radiology$', views.RadiologyAdd.as_view(), name='radiology_add'),
    url(r'^patient/[0-9]+/radiology/(?P<pk>[0-9]+)$', views.RadiologyEdit.as_view(), name='radiology_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/echocardiography$', views.EchocardiographyAdd.as_view(), name='echocardiography_add'),
    url(r'^patient/[0-9]+/echocardiography/(?P<pk>[0-9]+)$', views.EchocardiographyEdit.as_view(), name='echocardiography_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/interven_rad$', views.Interventional_RadiologyAdd.as_view(), name='interven_rad_add'),
    url(r'^patient/[0-9]+/interven_rad/(?P<pk>[0-9]+)$', views.Interventional_RadiologyEdit.as_view(), name='interven_rad_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/routine_lab$', views.routine_lab, name='routine_lab'),

    url(r'^patient/(?P<patient_id>[0-9]+)/lab_qual$', views.Lab_QualAdd.as_view(), name='lab_qual_add'),
    url(r'^patient/[0-9]+/lab_qual/(?P<pk>[0-9]+)$', views.Lab_QualEdit.as_view(), name='lab_qual_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/lab_quant$', views.Lab_QuantAdd.as_view(), name='lab_quant_add'),
    url(r'^patient/lab_quant/(?P<pk>[0-9]+)$', views.Lab_QuantEdit.as_view(), name='lab_quant_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/culture$', views.CultureAdd.as_view(), name='culture_add'),
    url(r'^patient/[0-9]+/culture/(?P<pk>[0-9]+)$', views.CultureEdit.as_view(), name='culture_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/fluid_analysis$', views.Fluid_analysisAdd.as_view(), name='fluid_analysis_add'),
    url(r'^patient/[0-9]+/fluid_analysis/(?P<pk>[0-9]+)$', views.Fluid_analysisEdit.as_view(), name='fluid_analysis_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/procedure$', views.ProcedureAdd.as_view(), name='procedure_add'),
    url(r'^patient/[0-9]+/procedure/(?P<pk>[0-9]+)$', views.ProcedureEdit.as_view(), name='procedure_edit'),

    url(r'^patient/(?P<patient_id>[0-9]+)/surgery$', views.SurgeryAdd.as_view(), name='surgery_add'),
    url(r'^patient/[0-9]+/surgery/(?P<pk>[0-9]+)$', views.SurgeryEdit.as_view(), name='surgery_edit'),
]
