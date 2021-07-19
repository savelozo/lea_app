from django.urls import path
from . import views

urlpatterns = [
    path('api/peer_review/', views.PeerListCreate.as_view() ),
    path('api/arts/', views.ArtListCreate.as_view() ),
    path('api/make_assigns/', views.MakeAssigns ),
    path('api/students/', views.StudentListCreate.as_view() )
]