from django.urls import path, include

from rest_framework.routers import DefaultRouter

from main.api import (
	ClientListView,
	CreateFaceLivenessSessionView,
	GetFaceLivenessSessionResultsView,
    ClientDetailView,
    ClientViewSet,
)

router = DefaultRouter()

router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('rekognition/session/', CreateFaceLivenessSessionView.as_view(), name='create_session'),
    path('rekognition/session/<str:session_id>/', GetFaceLivenessSessionResultsView.as_view(), name='get_session_results'),
    path('clients/<str:id_document>/', ClientDetailView.as_view(), name='client-detail'),
    path('crud-clients/', include(router.urls)),
]