# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.IntegerField()

    def __str__(self):
        return self.address1

class Company(models.Model):
    """This class represents a company"""
    name = models.CharField(max_length=100, blank=False)
    address = models.ForeignKey(Address,)
    def __str__(self):
        return self.name


class Profile(models.Model):
    """store the user's company"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    company = models.ForeignKey(Company,
        on_delete=models.CASCADE,)

    def __str__(self):
        return self.user.username

class CostCenter(models.Model):
    name = models.CharField(max_length=100, blank=False)
    company = models.ForeignKey(Company,
        on_delete=models.CASCADE)
    address = models.ForeignKey(Address,
        blank=True)

    def __str__(self):
        return self.name

class MailPiece(models.Model):
    user = models.ForeignKey(User,)
    cost_center = models.ForeignKey(CostCenter,)
    address = models.ForeignKey(Address,)
    return_address = models.ForeignKey(Address, related_name='+')
    rate = models.IntegerField()
    mail_class = models.CharField(max_length=100,)
    tracking = models.IntegerField()

    def __str__(self):
        return str(self.tracking)
