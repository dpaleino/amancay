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
from bts_queries import soap_queries

def render_bug_table(request, queries, title, bugs, amount):
	if (bugs != None and len(bugs) > 0):
		bug_list = queries.get_bugs_status(bugs[:amount])
	else:
		bug_list = None
	if (request.GET.has_key('xhr')):
		return HttpResponse( simplejson.dumps(bug_list),
		                     mimetype='application/javascript' )
	elif (request.path.find("table") != -1):
		return render_to_response('table.html', 
		                          {'bug_list': bug_list,
		                           'table_title': title }
		                         )
	else:
		return render_to_response('index.html', 
		                          {'bug_list': bug_list,
		                           'table_title': title,
								   'current_user': request.user}
		                         )


def submitted_bugs(request):
	user = request.user
	queries = soap_queries()
	if (user.is_authenticated()):
		bugs = queries.get_submitters_bugs(user.email)
	else:
		submitter_emails = request.session.get('submitter_emails')
		bugs = queries.get_submitters_bugs(submitter_emails)
	return render_bug_table(request, queries, "Latest submitted bugs",
	bugs, 15)

def received_bugs(request):
	user = request.user
	queries = soap_queries()
	if (user.is_authenticated()):
		bugs = queries.get_maintainers_bugs(user.email)
	else:
		maintainer_emails = request.session.get('maintainer_emails')
		bugs = queries.get_maintainers_bugs(maintainer_emails)
	bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest received bugs", bugs,
	15)
		
def package_bugs(request):
	user = request.user
	queries = soap_queries()
	if (user.is_authenticated()):
		package_list = request.user.package_set.all()
		package_list = [ p.package_name for p in package_list]
	else:
		package_list = request.session.get('packages')
	bugs = queries.get_packages_bugs(package_list)
	bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest bugs on selected packages", bugs, 15)

def selected_bugs(request):
	user = request.user
	queries = soap_queries()
	if (user.is_authenticated()):
		bugs = [b.number for b in request.user.bug_set.all()]
	else:
		bugs = request.session.get('bugs')
	if (bugs != None):
		bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest selected bugs", bugs,
	15)
