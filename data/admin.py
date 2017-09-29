# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from data.models import Company, Profile, Address, CostCenter, MailPiece

# Register your models here.
admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(CostCenter)
admin.site.register(MailPiece)
