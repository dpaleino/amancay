from django.conf.urls.defaults import *

urlpatterns = patterns('',
	# Normal pages
	(r'^$', 'amancay.views.index',),
	(r'^index', 'amancay.views.index',),

	# Toolboxes
	(r'toolbox', 'amancay.toolbox.render_toolbox',),

	# Bug pages
	(r'^package_bugs', 'amancay.tables.package_bugs',),
	(r'^received_bugs', 'amancay.tables.received_bugs',),
	(r'^search', 'amancay.search.search',),
	(r'^selected_bugs', 'amancay.tables.selected_bugs',),
	(r'^submitted_bugs', 'amancay.tables.submitted_bugs',),
	(r'^tagged_bugs', 'amancay.tables.tagged_bugs',),

	# Inside pages
	(r'^(?P<bug_number>\d+)/?$', 'amancay.bugs.bug',),
	(r'^bug/(?P<bug_number>\d+)', 'amancay.bugs.bug',),
	(r'^package/(?P<package_name>\w+)', 'amancay.views.package',),

	# Small pieces
	(r'^ajax/package/add/', 'amancay.ajax.package_add',),
	(r'^ajax/package/remove/', 'amancay.ajax.package_remove',),
	(r'^ajax/bug/subscribe/', 'amancay.ajax.bug_subscribe',),
	(r'^ajax/bug/unsubscribe/', 'amancay.ajax.bug_unsubscribe',),
	(r'^ajax/bug/add/', 'amancay.ajax.bug_add',),
	(r'^ajax/bug/remove/', 'amancay.ajax.bug_remove',),

	# Account Settings
	#   (r'^account_settings', 'amancay.views.account_settings',),

	# Activate a pending message
	(r'^send_message/(?P<activation_key>\w+)/$', 'amancay.bugs.activate_message',),

	# MochiKit and other static pages
	(r'^images/(.*)$', 'django.views.static.serve',
		{'document_root': 'amancay/images/'}),
	(r'^static/(.*)$', 'django.views.static.serve',
		{'document_root': 'amancay/static/'}),

	# Uncomment this for admin:
	#   (r'^admin/', include('django.contrib.admin.urls')),
)
