from rest_framework import serializers
from .models import Company, Profile, Address, MailPiece, CostCenter
from django.contrib.auth.models import User

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('pk', 'address1','address2', 'city', 'state', 'zip',)

class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Company
        fields = ('pk', 'id', 'name', 'address',)

    def create(self, request):
        request['address'] = Address.objects.create(
            **request.pop('address'))
        return super(CompanySerializer, self).create(request)

    def update(self, instance, request):
        if 'address' in request:
            request['address'] = Address.objects.create(
                **request.pop('address'))
        return super(CompanySerializer, self).update(instance, request)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('pk', 'user', 'company',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'id', 'username',)

class MailPieceSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    return_address = AddressSerializer()
    class Meta:
        model = MailPiece
        fields = ('pk', 'user', 'cost_center', 'address', 'return_address',
            'rate', 'mail_class', 'tracking',)
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['address'] = Address.objects.create(
            **validated_data.pop('address'))
        validated_data['return_address'] = Address.objects.create(
            **validated_data.pop('return_address'))
        return MailPiece.objects.create(**validated_data)

    def update(self, instance, request):
        if 'address' in request:
            request['address'] = Address.objects.create(
                **request.pop('address'))
        if 'return_address' in request:
            request['return_address'] = Address.objects.create(
                **request.pop('return_address'))
        return super(MailPieceSerializer, self).update(instance, request)

class CostCenterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = CostCenter
        fields = ('pk', 'name', 'company', 'address',)
        read_only_fields = ('company',)

    def create(self, validated_data):
        validated_data['address'] = Address.objects.create(
            **validated_data.pop('address'))
        return CostCenter.objects.create(**validated_data)

    def update(self, instance, request):
        if 'address' in request:
            request['address'] = Address.objects.create(
                **request.pop('address'))
        return super(CostCenterSerializer, self).update(instance, request)
