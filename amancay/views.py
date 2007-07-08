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

def index(request):
	if request.POST:
		if (request.POST.has_key('package_name')):
			add_package(request)
		if (request.POST.has_key('package_select')):
			remove_packages(request)
		if (request.POST.has_key('bug_number')):
			add_bug(request)
		if (request.POST.has_key('bug_select')):
			remove_bugs(request)
	user = request.user
	if (user.is_authenticated()):
		package_list = request.user.package_set.all()
		package_list = [ p.package_name for p in package_list]
		bug_list = [b.number for b in request.user.bug_set.all()]
	else:
		package_list = request.session.get('packages')
		bug_list = request.session.get('bugs')

	# Check if it's AJAX or HTML
	if (request.GET.has_key('xhr')):
		return HttpResponse( simplejson.dumps({"package_list":
		package_list, "bug_list": bug_list}),
		                     mimetype='application/javascript' )
	else:
		return render_to_response('index.html', 
		                          {'package_list': package_list,
		                           'bug_list': bug_list, 
		                           'current_user': user}
		                         )
def add_package(request):
	user = request.user
	package_name = request.POST['package_name']
	if (user.is_authenticated()):
		packages = user.package_set.filter(package_name=package_name)
		if (len(packages) == 0):
			user.package_set.create(package_name=package_name)
	else:
		packages = request.session.get('packages')
		if (packages == None):
			packages = request.session['packages'] = []
		for package in packages:
			if (package == package_name):
				return 
		request.session['packages'].append(package_name)

def remove_packages(request):
	user = request.user
	package_selected = request.POST.getlist("package_select")
	if (user.is_authenticated()):
		for package_name in package_selected:
			packages = user.package_set.filter(package_name=package_name)
			if (len(packages) != 0):
				packages[0].delete()
	else:
		packages = request.session.get('packages')
		if (packages == None):
			packages = request.session['packages'] = []
		else:
			for package_name in package_selected:
				for package in packages:
					if (package == package_name):
						request.session['packages'].remove(package_name)

def add_bug(request):
	user = request.user
	bug_number = request.POST['bug_number']
	if (user.is_authenticated()):
		bugs = user.bug_set.filter(number=bug_number)
		if (len(bugs) == 0):
			user.bug_set.create(number=bug_number)
	else:
		bugs = request.session.get('bugs')
		if (bugs == None):
			bugs = request.session['bugs'] = []
		for bug in bugs:
			if (bug == bug_number):
				return 
		request.session['bugs'].append(bug_number)

def remove_bugs(request):
	user = request.user
	bug_selected = request.POST.getlist("bug_select")
	if (user.is_authenticated()):
		for number in bug_selected:
			bugs = user.bug_set.filter(number=number)
			if (len(bugs) != 0):
				bugs[0].delete()
	else:
		bugs = request.session.get('bugs')
		if (bugs == None):
			bugs = request.session['bugs'] = []
		else:
			for bug_number in bug_selected:
				for bug in bugs:
					if (bug == bug_number):
						request.session['bugs'].remove(bug_number)

# Package page

def package(request, package_name):
	user = request.user
	queries = soap_queries()

	bugs = queries.get_packages_bugs(package_name)
	bugs.sort(reverse=True)
	bug_list = queries.get_bugs_status(bugs)

	# Check if it's AJAX or HTML
	if (request.GET.has_key('xhr')):
		return HttpResponse( simplejson.dumps({"package":
		package_name, "bug_list": bug_list}),
		                     mimetype='application/javascript' )
	else:
		return render_to_response('package.html', 
		                          {'package': package_name,
		                           'bug_list': bug_list, 
		                           'current_user': user}
		                         )

