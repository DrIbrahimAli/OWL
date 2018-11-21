from django.urls import path, include
from . import views

app_name='tasks'
urlpatterns = [
    path('add', views.TaskAdd.as_view(), name='task_add'),
    path('edit/<int:pk>', views.TaskEdit.as_view(), name='task_edit'),
    path('comment/<int:pk>', views.TaskComment.as_view(), name='task_comment'),
    path('do/<int:pk>', views.TaskDone.as_view(), name='task_done'),
    path('list/undone', views.TaskList.as_view(), name='tasks_undone'),
    path('list/all', views.TaskAll.as_view(), name='tasks_all'),
    ]
