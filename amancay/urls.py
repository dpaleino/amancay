# vim: set sw=4 ts=4 sts=4 noet:
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$',     'amancay.views.index',),
    (r'^index', 'amancay.views.index',),

    (r'^search',            'amancay.search.search',),

    (r'^bugs/packages',     'amancay.tables.package_bugs',),
    (r'^bugs/received',     'amancay.tables.received_bugs',),
    (r'^bugs/selected',     'amancay.tables.selected_bugs',),
    (r'^bugs/submitted',    'amancay.tables.submitted_bugs',),
    (r'^bugs/tagged',       'amancay.tables.tagged_bugs',),

    # Inside pages
    (r'^(?P<bug_number>\d+)/?$',        'amancay.bugs.bug',),
    (r'^bug/(?P<bug_number>\d+)',       'amancay.bugs.bug',),
    (r'^package/(?P<package_name>[\w-]+)', 'amancay.views.package',),

    # Small pieces for AJAX
    (r'^ajax/package/add/',     'amancay.ajax.package_add',),
    (r'^ajax/bug/add/',         'amancay.ajax.bug_add',),
    (r'^ajax/maintainer/add/',  'amancay.ajax.maintainer_add',),
    (r'^ajax/submitter/add/',   'amancay.ajax.submitter_add',),
    (r'^ajax/user/add/',        'amancay.ajax.user_add',),

    (r'^ajax/package/remove/',      'amancay.ajax.package_remove',),
    (r'^ajax/bug/remove/',          'amancay.ajax.bug_remove',),
    (r'^ajax/maintainer/remove/',   'amancay.ajax.maintainer_remove',),
    (r'^ajax/submitter/remove/',    'amancay.ajax.submitter_remove',),
    (r'^ajax/user/remove/',         'amancay.ajax.user_remove',),

    (r'^ajax/bug/subscribe/',   'amancay.ajax.bug_subscribe',),
    (r'^ajax/bug/unsubscribe/', 'amancay.ajax.bug_unsubscribe',),

    # Account Settings
    #   (r'^account_settings', 'amancay.views.account_settings',),

    # Activate a pending message
    (r'^send_message/(?P<activation_key>\w+)/$', 'amancay.bugs.activate_message',),

    # MochiKit and other static pages
    (r'^images/(.*)$', 'django.views.static.serve',
        {'document_root': 'amancay/images/'}),
    (r'^static/(.*)$', 'django.views.static.serve',
        {'document_root': 'amancay/static/'}),
)
