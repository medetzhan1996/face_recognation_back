from django.urls import path
from main.api import (
	ClientListView,
	CreateFaceLivenessSessionView,
	GetFaceLivenessSessionResultsView,
    ClientDetailView,
)

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('rekognition/session/', CreateFaceLivenessSessionView.as_view(), name='create_session'),
    path('rekognition/session/<str:session_id>/', GetFaceLivenessSessionResultsView.as_view(), name='get_session_results'),
    path('clients/<str:id_document>/', ClientDetailView.as_view(), name='client-detail'),
]