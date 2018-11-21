from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from ckeditor.widgets import CKEditorWidget
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('done',)
        widgets = {
        'due_date': AdminDateWidget,
        'description': forms.Textarea,
        'comments': CKEditorWidget,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('comments',)
        widgets = {
        'comments': forms.Textarea,
        }
