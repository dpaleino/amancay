from django.conf.urls.defaults import *

urlpatterns = patterns('',

	# Normal pages
	(r'^$', 'bts_webui.amancay.views.index',),
	(r'^index', 'bts_webui.amancay.views.index',),

	# Toolboxes
	(r'toolbox', 'bts_webui.amancay.toolbox.render_toolbox',),

	# Bug pages
	(r'^submitted_bugs', 'bts_webui.amancay.tables.submitted_bugs',),
	(r'^received_bugs', 'bts_webui.amancay.tables.received_bugs',),
	(r'^package_bugs', 'bts_webui.amancay.tables.package_bugs',),
	(r'^selected_bugs', 'bts_webui.amancay.tables.selected_bugs',),
	(r'^tagged_bugs', 'bts_webui.amancay.tables.tagged_bugs',),
	(r'^search', 'bts_webui.amancay.search.search',),

	# Inside pages
	(r'^package/(?P<package_name>\w+)', 'bts_webui.amancay.views.package',),
	(r'^bug/(?P<bug_number>\d+)', 'bts_webui.amancay.bugs.bug',),
	(r'^(?P<bug_number>\d+)/?$', 'bts_webui.amancay.bugs.bug',),

	# Small pieces
	(r'^add_package', 'bts_webui.amancay.views.add_package',),

	# Account Settings
	(r'^account_settings', 'bts_webui.amancay.views.account_settings',),
	
	# Activate a pending message
	(r'^send_message/(?P<activation_key>\w+)/$', 'bts_webui.amancay.bugs.activate_message',),

	# MochiKit and other static pages
	(r'^static/(.*)$', 'django.views.static.serve', {'document_root':
	'amancay/static/'}),
	(r'^images/(.*)$', 'django.views.static.serve', {'document_root':
	'amancay/images/'}),
    
	# Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
