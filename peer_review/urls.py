from django.urls import path
from . import views

urlpatterns = [
    path('api/courses/', views.CourseListCreate.as_view() ),
    path('api/arts/', views.ArtListCreate.as_view() ),
    path('api/make_assigns/', views.MakeAssigns ),
    path('api/students/', views.StudentListCreate.as_view() )
]