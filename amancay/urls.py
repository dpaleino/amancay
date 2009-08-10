from django.conf.urls.defaults import *

urlpatterns = patterns('',
	# Normal pages
	(r'^$', 'bts_webui.amancay.views.index',),
	(r'^index', 'bts_webui.amancay.views.index',),

	# Toolboxes
	(r'toolbox', 'bts_webui.amancay.toolbox.render_toolbox',),

	# Bug pages
	(r'^package_bugs', 'bts_webui.amancay.tables.package_bugs',),
	(r'^received_bugs', 'bts_webui.amancay.tables.received_bugs',),
	(r'^search', 'bts_webui.amancay.search.search',),
	(r'^selected_bugs', 'bts_webui.amancay.tables.selected_bugs',),
	(r'^submitted_bugs', 'bts_webui.amancay.tables.submitted_bugs',),
	(r'^tagged_bugs', 'bts_webui.amancay.tables.tagged_bugs',),

	# Inside pages
	(r'^(?P<bug_number>\d+)/?$', 'bts_webui.amancay.bugs.bug',),
	(r'^bug/(?P<bug_number>\d+)', 'bts_webui.amancay.bugs.bug',),
	(r'^package/(?P<package_name>\w+)', 'bts_webui.amancay.views.package',),

	# Small pieces
	(r'^ajax/package/add/', 'bts_webui.amancay.ajax.package_add',),
	(r'^ajax/package/remove/', 'bts_webui.amancay.ajax.package_remove',),
	(r'^ajax/bug/subscribe/', 'bts_webui.amancay.ajax.bug_subscribe',),
	(r'^ajax/bug/unsubscribe/', 'bts_webui.amancay.ajax.bug_unsubscribe',),
	(r'^ajax/bug/add/', 'bts_webui.amancay.ajax.bug_add',),
	(r'^ajax/bug/remove/', 'bts_webui.amancay.ajax.bug_remove',),

	# Account Settings
	#   (r'^account_settings', 'bts_webui.amancay.views.account_settings',),

	# Activate a pending message
	(r'^send_message/(?P<activation_key>\w+)/$', 'bts_webui.amancay.bugs.activate_message',),

	# MochiKit and other static pages
	(r'^images/(.*)$', 'django.views.static.serve',
		{'document_root': 'amancay/images/'}),
	(r'^static/(.*)$', 'django.views.static.serve',
		{'document_root': 'amancay/static/'}),

	# Uncomment this for admin:
	#   (r'^admin/', include('django.contrib.admin.urls')),
)
