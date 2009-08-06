# vim: set sw=4 ts=4 sts=4 noet:
import datetime

# Needed to get_template, prepare context and output Response
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

# Shortcut for rendering a response
from django.shortcuts import get_object_or_404, render_to_response

# Model clases
from django.contrib.auth.models import User
from bts_webui.amancay.models import Package

# Needed for AJAX
from django.utils import simplejson

# Needed for SOAP
from bts_queries import SoapQueries

# Tables POST processing
from tables import process_post, selected_bugs
from search import search

def index(request):
	"""
	Our pretty useless index page.
	"""
	if request.user:
		user = request.user
	else:
		user = None

	return render_to_response('home.html',
							  {'user': user,}
							 )

def package(request, package_name):
	"""
	Individual package page.
	"""
	user = request.user
	queries = SoapQueries()

	bugs = queries.get_packages_bugs(package_name)
	bugs.sort(reverse=True)
	bug_list = queries.get_bugs_status(bugs)

	# Check if it's AJAX or HTML
	if request.GET.has_key('xhr'):
		return HttpResponse(simplejson.dumps({"package": package_name,
											  "bug_list": bug_list}),
							mimetype='application/javascript')
	else:
		return render_to_response('package.html',
								  {'package': package_name,
								   'bug_list': bug_list,
								   'current_user': user}
								 )
