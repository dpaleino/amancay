from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^$', 'bts_webui.amancay.views.index',),
	(r'^index', 'bts_webui.amancay.views.index',),
	(r'^add_package', 'bts_webui.amancay.views.add_package',),
	(r'^submitted_bugs', 'bts_webui.amancay.views.submitted_bugs',),
	(r'^received_bugs', 'bts_webui.amancay.views.received_bugs',),
	(r'^package_bugs', 'bts_webui.amancay.views.package_bugs',),
	(r'^selected_bugs', 'bts_webui.amancay.views.selected_bugs',),
	
	# MochiKit and other static pages
	(r'^static/(.*)$', 'django.views.static.serve', {'document_root':
	'amancay/static/'}),
    
	# Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
