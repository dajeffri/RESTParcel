from data.models import Company, Profile, Address, MailPiece, CostCenter
from data.serializers import (CompanySerializer, ProfileSerializer,
UserSerializer, AddressSerializer, CostCenterSerializer, MailPieceSerializer)
from data.permissions import IsAdminOrReadOnly, IsCompany, IsUser
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


class CompanyViewSet(viewsets.ModelViewSet):
    """
    List and detail from Company that the user works for.
    """
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(pk=self.request.user.profile.company.pk)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    List and detail from Profiles from the users company
    TODO remove before production, leaving for development
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(company=self.request.user.profile.company)

class UserViewSet(viewsets.ModelViewSet):
    """
    List and detail from Users from the users company
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(profile__company=self.request.user.profile.company)

    def create(self, request):
        """
        Create profile for user
        """
        new_user = super(UserViewSet, self).create(request)
        profile = Profile.objects.create(
            user=User.objects.get(pk=new_user.data['pk']),
            company=self.request.user.profile.company)
        return new_user


class AddressViewSet(viewsets.ModelViewSet):
    """
    List and detail from Address
    TODO remove before production, leaving for development
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CostCenterViewSet(viewsets.ModelViewSet):
    """
    List and detail from CostCenters from the users company
    """
    permission_classes = (permissions.IsAuthenticated, IsCompany)
    serializer_class = CostCenterSerializer

    def get_queryset(self):
        return CostCenter.objects.filter(company=self.request.user.profile.company)

    def perform_create(self, serializer):
        """automatically add company"""
        serializer.validated_data['company'] = self.request.user.profile.company
        return super(CostCenterViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        """automatically add company"""
        serializer.validated_data['company'] = self.request.user.profile.company
        return super(CostCenterViewSet, self).perform_update(serializer)

class MailPieceViewSet(viewsets.ModelViewSet):
    """
    List and detail from MailPiece from the users company
    """
    permission_classes = (permissions.IsAuthenticated, IsUser)
    serializer_class = MailPieceSerializer

    def get_queryset(self):
        return MailPiece.objects.filter(user__profile__company=self.request.user.profile.company)

    def perform_create(self, serializer):
        """automatically add user"""
        serializer.validated_data['user'] = self.request.user
        return super(MailPieceViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        """automatically add user"""
        serializer.validated_data['user'] = self.request.user
        return super(MailPieceViewSet, self).perform_update(serializer)

@api_view(['GET'])
def data_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'company': reverse('company-list', request=request, format=format),
        'address': reverse('address-list', request=request, format=format),
        'costcenter': reverse('costcenter-list', request=request, format=format),
        'mailpiece': reverse('mailpiece-list', request=request, format=format),
    })
