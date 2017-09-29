from django.conf.urls import url, include
from data.views import (CompanyViewSet, ProfileViewSet, UserViewSet,
AddressViewSet, CostCenterViewSet, MailPieceViewSet)
from rest_framework import renderers
from data import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'company', views.CompanyViewSet, 'Company')
router.register(r'users', views.UserViewSet, 'User')
router.register(r'profile', views.ProfileViewSet, 'Profile')
router.register(r'address', views.AddressViewSet, 'Address') #Remove before production
router.register(r'costcenter', views.CostCenterViewSet, 'CostCenter')
router.register(r'mailpiece', views.MailPieceViewSet, 'MailPiece')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
