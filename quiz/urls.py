from django.conf.urls import patterns, url

from .views import QuizListView, CategoriesListView,\
    ViewQuizListByCategory, QuizUserProgressView, QuizMarkingList,\
    QuizMarkingDetail, QuizDetailView, QuizTake


urlpatterns = [

                       url(r'^$',
                           QuizListView.as_view(),
                           name='quiz_index'),

                       url(r'^category/$',
                           CategoriesListView.as_view(),
                           name='quiz_category_list_all'),

                       url(r'^category/(?P<category_name>[\w|\W-]+)/$',
                           ViewQuizListByCategory.as_view(),
                           name='quiz_category_list_matching'),

                       url(r'^progress/$',
                           QuizUserProgressView.as_view(),
                           name='quiz_progress'),

                       url(r'^marking/$',
                           QuizMarkingList.as_view(),
                           name='quiz_marking'),

                       url(r'^marking/(?P<pk>[\d.]+)/$',
                           QuizMarkingDetail.as_view(),
                           name='quiz_marking_detail'),

                       #  passes variable 'quiz_name' to quiz_take view
                       url(r'^(?P<slug>[\w-]+)/$',
                           QuizDetailView.as_view(),
                           name='quiz_start_page'),

                       url(r'^(?P<quiz_name>[\w-]+)/take/$',
                           QuizTake.as_view(),
                           name='quiz_question'),
]
