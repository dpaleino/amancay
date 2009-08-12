# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from amancay.btsqueries import SoapQueries

def _get_bug_list(request, view):
	"""
	Process the requested bug list corresponding to a given view.
	"""
	queries = SoapQueries()
	bugs = bug_list = []

	if view == 'received_bugs':
		if request.user.is_authenticated():
			user_emails = [e.address for e in request.user.useremail_set.all()]
		else:
			user_emails = request.session.get('maintaineremail_set')

		bugs = queries.get_tagged_bugs(user_emails)

	elif view == 'submitted_bugs':
		if request.user.is_authenticated():
			submitter_emails = [e.address for e in request.user.submitteremail_set.all()]
		else:
			submitter_emails = request.session.get('submitteremail_set')

		bugs = queries.get_submitters_bugs(submitter_emails)

	elif view == 'selected_bugs':
		if request.user.is_authenticated():
			bugs = [b.number for b in request.user.bug_set.all()]
		else:
			bugs = request.session.get('bug_set')

	elif view == 'package_bugs':
		if request.user.is_authenticated():
			package_list = [p.package_name for p in request.user.package_set.all()]
		else:
			package_list = request.session.get('package_set')

		bugs = queries.get_packages_bugs(package_list)

	elif view == 'tagged_bugs':
		if request.user.is_authenticated():
			user_emails = [e.address for e in request.user.useremail_set.all()]
		else:
			user_emails = request.session.get('useremail_set')

		bugs = queries.get_tagged_bugs(user_emails)

	if bugs:
		bug_list = queries.get_bugs_status(bugs[:15])
		bug_list.sort(key=lambda x: x.package)

	return bug_list

def received_bugs(request):
	"""
	Render a table view for bugs we have received as maintainers.
	"""
	bug_list = _get_bug_list(request, 'received_bugs')

	return render_to_response('table.html',
							  {'title': 'Latest received bugs',
							   'bug_list': bug_list,
							   'current_view': 'received_bugs'},
							  context_instance=RequestContext(request))

def submitted_bugs(request):
	"""
	Render a table view for bugs we have submitted ourselves.
	"""
	bug_list = _get_bug_list(request, 'submitted_bugs')

	return render_to_response('table.html',
							  {'title': 'Latest submitted bugs',
							   'bug_list': bug_list,
							   'current_view': 'submitted_bugs'},
							  context_instance=RequestContext(request))

def selected_bugs(request):
	"""
	Render a table view for bugs we are watching.
	"""
	bug_list = _get_bug_list(request, 'selected_bugs')

	return render_to_response('table.html',
							  {'title': 'Latest selected bugs',
							   'bug_list': bug_list,
							   'current_view': 'selected_bugs'},
							  context_instance=RequestContext(request))

def package_bugs(request):
	"""
	Render a table view for our watched packages.
	"""
	if request.user.is_authenticated():
		package_list = [p.package_name for p in request.user.package_set.all()]
	else:
		package_list = request.session.get('package_set', [])

	bug_list = _get_bug_list(request, 'package_bugs')

	for bug in bug_list:
		if bug.package in package_list:
			bug.pkg_fav = True
		else:
			bug.pkg_fav = False

	return render_to_response('table.html',
							  {'title': 'Latest bugs on selected packages',
							   'bug_list': bug_list,
							   'current_view': 'package_bugs'},
							  context_instance=RequestContext(request))

def tagged_bugs(request):
	"""
	Render a table view for bugs we have tagged.
	"""
	bug_list = _get_bug_list(request, 'tagged_bugs')

	# TODO: fix this, bugs is a dict where every value is a dict of tags and
	# bugs associated to one mail
	return render_to_response('table.html',
							  {'title': 'Latest received bugs',
							   'bug_list': bug_list,
							   'current_view': 'tagged_bugs'},
							  context_instance=RequestContext(request))
