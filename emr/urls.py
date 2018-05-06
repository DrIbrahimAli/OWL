from django.urls import path, include
from . import views

app_name='emr'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('physician/add', views.PhysicianAdd.as_view(), name='physician_add'),
    path('physician/<int:pk>/edit', views.PhysicianEdit.as_view(), name='physician_edit'),

    path('patient/search', views.PatientSearch.as_view(), name='patient_search'),

    path('patient/add', views.PatientAdd.as_view(), name='patient_add'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/edit', views.PatientEdit.as_view(), name='patient_edit'),

    path('patient/<int:patient_id>/admit', views.PatientAdmit.as_view(), name='patient_admit'),
    path('admission/<int:pk>', views.AdmissionEdit.as_view(), name='admission_edit'),

    path('patient/<int:patient_id>/discharge', views.PatientDischarge.as_view(), name='patient_discharge'),
    path('discharge/<int:pk>', views.DischargeEdit.as_view(), name='discharge_edit'),
    path('discharge_summary/<int:pk>', views.dischargeSummary, name='discharge_summary'),

    path('patient/<int:patient_id>/history', views.HistoryAdd.as_view(), name='history_add'),
    path('history/<int:pk>', views.HistoryEdit.as_view(), name='history_edit'),

    path('patient/<int:patient_id>/note', views.NoteAdd.as_view(), name='note_add'),
    path('note/<int:pk>', views.NoteEdit.as_view(), name='note_edit'),

    path('patient/<int:patient_id>/radiology', views.RadiologyAdd.as_view(), name='radiology_add'),
    path('radiology/<int:pk>', views.RadiologyEdit.as_view(), name='radiology_edit'),

    path('patient/<int:patient_id>/echocardiography', views.EchocardiographyAdd.as_view(), name='echocardiography_add'),
    path('echocardiography/<int:pk>', views.EchocardiographyEdit.as_view(), name='echocardiography_edit'),

    path('patient/<int:patient_id>/interven_rad', views.Interventional_RadiologyAdd.as_view(), name='interven_rad_add'),
    path('interven_rad/<int:pk>', views.Interventional_RadiologyEdit,name='interven_rad_edit'),

    path('patient/<int:patient_id>/routine_lab', views.routine_lab, name='routine_lab'),

    path('patient/<int:patient_id>/lab_qual', views.Lab_QualAdd.as_view(), name='lab_qual_add'),
    path('lab_qual/<int:pk>', views.Lab_QualEdit.as_view(), name='lab_qual_edit'),

    path('patient/<int:patient_id>/lab_quant', views.Lab_QuantAdd.as_view(), name='lab_quant_add'),
    path('lab_quant/<int:pk>', views.Lab_QuantEdit.as_view(), name='lab_quant_edit'),

    path('patient/<int:patient_id>/culture', views.CultureAdd.as_view(), name='culture_add'),
    path('culture/<int:pk>', views.CultureEdit.as_view(), name='culture_edit'),

    path('patient/<int:patient_id>/fluid_analysis', views.Fluid_analysisAdd.as_view(), name='fluid_analysis_add'),
    path('fluid_analysis/<int:pk>', views.Fluid_analysisEdit.as_view(), name='fluid_analysis_edit'),

    path('patient/<int:patient_id>/procedure', views.ProcedureAdd.as_view(), name='procedure_add'),
    path('procedure/<int:pk>', views.ProcedureEdit.as_view(), name='procedure_edit'),

    path('patient/<int:patient_id>/surgery', views.SurgeryAdd.as_view(), name='surgery_add'),
    path('surgery/<int:pk>', views.SurgeryEdit.as_view(), name='surgery_edit'),
]
