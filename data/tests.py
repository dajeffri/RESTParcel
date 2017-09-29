# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from data.models import Address, Company, Profile, CostCenter, MailPiece
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient

# Create your tests here.
class CompanyTest(APITestCase):
    """
    Test suite for company
    """
    fixtures = ['users.json', 'data.json']
    def setUp(self):
        """set up variables for multiple company tests"""
        self.admin = User.objects.get(username='admin')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.data = {'name': 'testCompany', 'address': {
            'address1': '123 fake st', 'address2': 'fake address 2',
            'city': 'nowhere', 'state': 'IN',  'zip': '90210'}}
        self.url = reverse('Company-list')

    def test_create_company(self):
        """
        Test company creation
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.latest('pk').name, 'testCompany')
        self.assertEqual(Address.objects.latest('pk').address1, '123 fake st')

    def test_company_permissions(self):
        """
        Test company permissions
        """
        testUser = User.objects.get(username="c1e1")
        client = APIClient()
        client.force_authenticate(user=testUser)
        response = client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_company_put(self):
        """
        Test company updates
        """
        companyPK = Company.objects.get(name=self.admin.profile.company.name).pk
        url = reverse('Company-detail', kwargs={'pk': companyPK})
        data = {'name': 'NewTestCompany', 'address': {'address1': '123 fake st',
            'address2': 'fake address 2',
            'city': 'nowhere', 'state': 'IN',  'zip': '90210'}}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=companyPK).name,
            'NewTestCompany')

    def test_company_patch(self):
        """
        Test company partial updates
        """
        companyPK = Company.objects.get(name=self.admin.profile.company.name).pk
        url = reverse('Company-detail', kwargs={'pk': companyPK})
        data = {'name': 'NewTestCompany'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=companyPK).name,
            'NewTestCompany')

    def test_company_put_permissions(self):
        """
        Test company update permissions
        """
        companyPK = Company.objects.get(name=self.admin.profile.company.name).pk
        url = reverse('Company-detail', kwargs={'pk': companyPK + 1})
        data = {'name': 'NewTestCompany', 'address': {'address1': '123 fake st',
            'address2': 'fake address 2',
            'city': 'nowhere', 'state': 'IN',  'zip': '90210'}}
        response = self.client.put(url, data, format='json')
        #This is 404 instead of 403 because there is no way to view a company
        #that you arent an employee of.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(Company.objects.get(pk=companyPK).name,
            'NewTestCompany')

    def test_company_patch_permissions(self):
        """
        Test company partial update permissions
        """
        companyPK = Company.objects.get(name=self.admin.profile.company.name).pk
        url = reverse('Company-detail', kwargs={'pk': companyPK + 1})
        data = {'name': 'NewTestCompany'}
        response = self.client.put(url, data, format='json')
        #This is 404 instead of 403 because there is no way to view a company
        #that you arent an employee of.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(Company.objects.get(pk=companyPK).name,
            'NewTestCompany')


class UserTest(APITestCase):
    """
    Test suite for user
    """
    fixtures = ['users.json', 'data.json']

    def setUp(self):
        """set up variables for multiple user tests"""
        self.testUser = User.objects.get(username="c1e1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.testUser)
        self.data = {'username': 'company1Test'}
        self.url = reverse('User-list')


    def test_user_create(self):
        """
        Test user creation
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.latest('pk').username, 'company1Test')
        self.assertEqual(Profile.objects.latest('pk').company,
            self.testUser.profile.company)

    def test_user_update(self):
        """
        Test user update
        testing put and patch together, because they are the same in this case.
        """
        userPK = self.testUser.pk
        url = reverse('User-detail', kwargs={'pk': userPK})
        data = {'username': 'company1NewTest'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=userPK).username,
            'company1NewTest')
        data = {'username': 'company1NewTest2'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=userPK).username,
            'company1NewTest2')

    def test_user_update_permissions(self):
        """
        Test user update
        testing put and patch together, because they are the same in this case.
        """
        userPK = User.objects.get(username='c2e1').pk
        url = reverse('User-detail', kwargs={'pk': userPK})
        data = {'username': 'company1NewTest'}
        response = self.client.put(url, data, format='json')
        #This is 404 instead of 403 because there is no way to view a company
        #that you arent an employee of.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(User.objects.get(pk=userPK).username,
            'company1NewTest')
        data = {'username': 'company1NewTest2'}
        response = self.client.patch(url, data, format='json')
        #This is 404 instead of 403 because there is no way to view a company
        #that you arent an employee of.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(User.objects.get(pk=userPK).username,
            'company1NewTest2')

class CostCenterTest(APITestCase):
    """
    Test suite for cost centers
    """
    fixtures = ['users.json', 'data.json']

    def setUp(self):
        """set up variables for multiple cost center tests"""
        self.testUser = User.objects.get(username="c1e1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.testUser)
        self.data = {'name': 'testCostCenter',
            'address': {'address1': '123 fake st', 'address2': 'fake address 2',
            'city': 'nowhere', 'state': 'IN',  'zip': '90210'}}
        self.url = reverse('CostCenter-list')

    def test_costcenter_create(self):
        """
        Test cost center creation
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CostCenter.objects.latest('pk').name, 'testCostCenter')

    def test_costcenter_permissions(self):
        """
        Test cost center permissions
        """
        self.data['company'] = User.objects.get(
            username='c2e1').profile.company.pk
        response = self.client.post(self.url, self.data, format='json')
        #cost center is created, but provided company is ignored.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(CostCenter.objects.latest('pk').company,
            self.data['company'])

    def test_costcenter_put(self):
        """
        Test cost center update
        """
        costCenterPK = CostCenter.objects.get(name='c1c1').pk
        url = reverse('CostCenter-detail', kwargs={'pk': costCenterPK})
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CostCenter.objects.get(pk=costCenterPK).name,
            'testCostCenter')

    def test_costcenter_patch(self):
        """
        Test cost center partial update
        """
        costCenterPK = CostCenter.objects.get(name='c1c1').pk
        url = reverse('CostCenter-detail', kwargs={'pk': costCenterPK})
        data = {'name': 'testCostCenter'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CostCenter.objects.get(pk=costCenterPK).name,
            'testCostCenter')

    def test_costcenter_put_permissions(self):
        """
        Test cost center update permissions
        """
        costCenterPK = CostCenter.objects.get(name='c2c1').pk
        url = reverse('CostCenter-detail', kwargs={'pk': costCenterPK})
        response = self.client.put(url, self.data, format='json')
        #This is 404 instead of 403 because there is no way to view a company
        #that you arent an employee of.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(CostCenter.objects.get(pk=costCenterPK).name,
            'testCostCenter')

    def test_costcenter_patch_permissions(self):
        """
        Test cost center partial update
        """
        costCenterPK = CostCenter.objects.get(name='c2c1').pk
        url = reverse('CostCenter-detail', kwargs={'pk': costCenterPK})
        data = {'name': 'testCostCenter'}
        response = self.client.patch(url, data, format='json')
        #This is 404 instead of 403 because there is no way to view a company
        #that you arent an employee of.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(CostCenter.objects.get(pk=costCenterPK).name,
            'testCostCenter')



class MailPieceTest(APITestCase):
    """
    Test suite for mail pieces
    """
    fixtures = ['users.json', 'data.json']

    def setUp(self):
        """set up variables for multiple mail piece tests"""
        self.testUser = User.objects.get(username="c1e1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.testUser)
        self.data = {
            "tracking": 1234,
            "mail_class": "12",
            "return_address": {
                "address1": "1234",
                "address2": "1234",
                "city": "1234",
                "state": "12",
                "zip": 1234
            },
            "rate": 1234,
            "address": {
                "address1": "1234",
                "address2": "1234",
                "city": "1234",
                "state": "12",
                "zip": 1234
            },
            "cost_center": CostCenter.objects.filter(company=
                self.testUser.profile.company.pk)[0].pk
        }
        self.url = reverse('MailPiece-list')

    def test_mailpiece_create(self):
        """
        Test mail piece creation
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MailPiece.objects.latest('pk').rate, 1234)

    def test_mailpiece_permissions(self):
        """
        Test mail piece permissions
        """
        self.data['user'] = User.objects.get(username='c2e1').pk
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(MailPiece.objects.latest('pk').user,
            self.data['user'])

    def test_mailpiece_put(self):
        """
        Test mail piece update
        """
        mailPiecePK = MailPiece.objects.filter(user=self.testUser.pk)[0].pk
        url = reverse('MailPiece-detail', kwargs={'pk': mailPiecePK})
        response = self.client.put(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MailPiece.objects.get(pk=mailPiecePK).tracking,
            1234)

    def test_mailpiece_patch(self):
        """
        Test mail piece partial update
        """
        mailPiecePK = MailPiece.objects.filter(user=self.testUser.pk)[0].pk
        url = reverse('MailPiece-detail', kwargs={'pk': mailPiecePK})
        data = {'tracking': 9876543210}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MailPiece.objects.get(pk=mailPiecePK).tracking,
            9876543210)

    def test_mailpiece_put_permissions(self):
        """
        Test mail piece update permissions
        """
        userPK = User.objects.get(username='c2e1').pk
        mailPiecePK = MailPiece.objects.filter(user=userPK)[0].pk
        url = reverse('MailPiece-detail', kwargs={'pk': mailPiecePK})
        self.data['user'] = userPK
        response = self.client.put(url, self.data, format='json')
        #This is 404 instead of 403 because there is no way to view a mail piece
        #that you arent the user on.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(MailPiece.objects.get(pk=mailPiecePK).user,
            self.data['user'])

    def test_mailpiece_patch_permissions(self):
        """
        Test mail piece partial update permissions
        """
        userPK = User.objects.get(username='c2e1').pk
        mailPiecePK = MailPiece.objects.filter(user=userPK)[0].pk
        url = reverse('MailPiece-detail', kwargs={'pk': mailPiecePK})
        data = {'tracking': 9876543210,
            'user': userPK}
        response = self.client.patch(url, data, format='json')
        #This is 404 instead of 403 because there is no way to view a mail piece
        #that you arent the user on.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(MailPiece.objects.get(pk=mailPiecePK).user,
            data['user'])
