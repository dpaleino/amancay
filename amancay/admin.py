# vim: set sw=4 ts=4 sts=4 noet:

from amancay.models import Package, Bug
from django.contrib import admin

admin.site.register(Package)
admin.site.register(Bug)
