# vim: set sw=4 ts=4 sts=4 noet:
from django.contrib import admin

from amancay.models import Package, Bug

admin.site.register(Package)
admin.site.register(Bug)
