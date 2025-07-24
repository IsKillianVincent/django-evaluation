from django.urls import path
from jobs.views import job_views, company_views, application_views


urlpatterns = [
    # Jobs
    path('', job_views.job_list, name='job_list'),
    path('job/<int:pk>/', job_views.job_detail, name='job_detail'),
    path('job/create/', job_views.create_job_view, name='create_job'),

    # Applications
    path('apply/<int:job_id>/', application_views.submit_application, name='submit_application'),
    path('my-applications/', application_views.user_applications, name='user_applications'),
    path('application/<int:app_id>/validate/', application_views.validate_application, name='validate_application'),
    path('application/<int:app_id>/invalidate/', application_views.invalidate_application, name='invalidate_application'),  

    path('employer/dashboard/', application_views.employer_dashboard, name='employer_dashboard'),

    # Companies
    path('companies/', company_views.company_list_view, name='company_list'),
    path('companies/create/', company_views.create_company_view, name='create_company'),
]
