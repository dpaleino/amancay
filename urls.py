from django.conf.urls.defaults import *

urlpatterns = patterns('',

	# The amancay app
	(r'^amancay/', include('bts_webui.amancay.urls')),

	# The registration app
	(r'^accounts/profile/', include('bts_webui.amancay.urls')),
	(r'^accounts/', include('bts_webui.registration.urls')),

	# Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

	# amancay is the main site here.
	(r'^/?', include('bts_webui.amancay.urls')),
    
)
