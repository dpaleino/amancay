# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from amancay.bts_queries import SoapQueries

def index(request):
	"""
	Our pretty useless index page.
	"""

	return render_to_response('home.html', {},
							  context_instance=RequestContext(request))

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
								   'bug_list': bug_list},
								  context_instance=RequestContext(request))
