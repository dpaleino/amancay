from django.conf.urls.defaults import *

# The next two lines enable the admin and load each admin.py file:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# The admin interface
	(r'^admin/(.*)', admin.site.root),

	# The amancay app
	(r'^amancay/', include('amancay.urls')),

	# The registration app
	(r'^accounts/profile/', include('amancay.urls')),
	(r'^accounts/', include('registration.urls')),

	# amancay is the main site here.
	(r'^/?', include('amancay.urls')),
    
)
