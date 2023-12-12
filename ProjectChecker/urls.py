from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.student_dashboard, name = 'student_dashboard'),
    path("lecturer_dashboard", views.lecturer_dashboard, name = 'lecturer_dashboard'),
    path('sessions/<int:pk>/', views.sessions, name = 'sessions'),
    path("login_user",views.login_user, name = "login_user"),
    path("login_select",views.login_select, name = "login_select"),
    path("logout_user",views.logout_user, name = "logout_user"),
    path("profile",views.profile, name = "profile"),
    path("student_signup",views.student_signup, name = "student_signup"),
    path("lecturer_signup",views.lecturer_signup, name = "lecturer_signup"),
    path("upload_project",views.upload_project, name = "upload_project"),
    path('approve_project/<int:project_id>/', views.approve_project, name = 'approve_project'),
    path('decline_project/<int:project_id>/', views.decline_project, name = 'decline_project'),
    path('approved_projects/<path:pk>/', views.approved_projects, name='approved_projects'),
    path('rejected_projects/<path:pk>/', views.rejected_projects, name = 'rejected_projects'),
    path('pending_projects/<path:pk>/', views.pending_projects, name = 'pending_projects'),
    path('project_detail/<int:pk>/', views.project_detail, name = 'project_detail'),

]

