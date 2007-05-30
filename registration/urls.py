"""
URLConf for Django user registration.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL begninning with
'/accounts/'.

"""

from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template
#from django.contrib.auth.views import login, logout
#from views import activate, register

urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]+ because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       (r'^activate/(?P<activation_key>\w+)/$',
					   'bts_webui.registration.views.activate'),
                       (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
                       (r'^register/$', 'bts_webui.registration.views.register'),
                       (r'^register/complete/$',
					   'django.views.generic.simple.direct_to_template', {'template': 'registration/registration_complete.html'}),
                       )
