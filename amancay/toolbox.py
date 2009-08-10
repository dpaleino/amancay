# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

def render_toolbox(request):
	toolbox = get_toolbox(request)
	return render_to_response('toolbox.html', {'toolbox': toolbox})

# FIXME:
# FIXME:
# FIXME: room for improvement.
def get_toolbox(request):
	# Initialization
	user = request.user
	toolbox = {}

	# Fill the info according to the type of toolbox needed
	if request.path.find('submitted_bugs') != -1:
		toolbox['title'] = 'Submitter emails'
		toolbox['item_type'] = 'submitter_email'

		if user.is_authenticated():
			email_list = request.user.submitteremail_set.all()
			toolbox['item_list'] = [e.address for e in email_list]
		else:
			toolbox['item_list'] = request.session.get('submitter_emails')
	
	# Received bugs
	elif request.path.find('received_bugs') != -1:
		toolbox['title'] = 'Maintainer emails'
		toolbox['item_type'] = 'maintainer_email'
		if user.is_authenticated():
			email_list = request.user.maintaineremail_set.all()
			toolbox['item_list'] = [e.address for e in email_list]
		else:
			toolbox['item_list'] = request.session.get('maintainer_emails')
	
	# Selected Packages
	elif request.path.find('package_bugs') != -1:
		toolbox['title'] = 'Selected Packages'
		toolbox['item_type'] = 'package'

		if user.is_authenticated():
			package_list = request.user.package_set.all()
			toolbox['item_list'] = [p.package_name for p in package_list]
		else:
			toolbox['item_list'] = request.session.get('packages')

	# Selected bugs
	elif request.path.find('selected_bugs') != -1:
		toolbox['title'] = 'Selected Bugs'
		toolbox['item_type'] = 'bug'

		if user.is_authenticated():
			bug_list = request.user.bug_set.all()
			toolbox['item_list'] = [b.number for b in bug_list]
		else:
			toolbox['item_list'] = request.session.get('bugs')
	
	# Tagged bugs
	elif request.path.find('tagged_bugs') != -1:
		toolbox['title'] = 'User emails'
		toolbox['item_type'] = 'user_email'

		if user.is_authenticated():
			email_list = request.user.useremail_set.all()
			toolbox['item_list'] = [e.address for e in email_list]
		else:
			toolbox['item_list'] = request.session.get('user_emails')
	
	# Done
	return toolbox

# FIXME:
# FIXME:
# FIXME:
# FIXME:
# FIXME:
# All this functions perhaps could be abstracted as a "Queue" class or
# something.
def add_package(request):
	"""
	Add a package to our session watched list.
	"""
	user = request.user
	package_name = request.POST['package_name']
	if user.is_authenticated():
		packages = user.package_set.filter(package_name=package_name)
		if not packages:
			user.package_set.create(package_name=package_name)
	else:
		packages = request.session.get('packages', [])
		for package in packages:
			if package == package_name:
				return 
		request.session['packages'].append(package_name)

def remove_packages(request):
	"""
	Remove a package from the watched list.
	"""
	user = request.user
	package_selected = request.POST.getlist('package_select')
	if user.is_authenticated():
		for package_name in package_selected:
			packages = user.package_set.filter(package_name=package_name)
			if packages:
				packages[0].delete()
	else:
		packages = request.session.get('packages', [])
		for package_name in package_selected:
			for package in packages:
				if (package == package_name):
					request.session['packages'].remove(package_name)

def add_bug(request):
	"""
	Add a bug to the session watched bugs.
	"""
	user = request.user
	bug_number = request.POST['bug_number']
	if user.is_authenticated():
		bugs = user.bug_set.filter(number=bug_number)
		if bugs:
			user.bug_set.create(number=bug_number)
	else:
		bugs = request.session.get('bugs', [])
		for bug in bugs:
			if bug == bug_number:
				return 
		request.session['bugs'].append(bug_number)

def remove_bugs(request):
	"""
	Remove the selected bugs from the session bug list.
	"""
	user = request.user
	bug_selected = request.POST.getlist('bug_select')
	if user.is_authenticated():
		for number in bug_selected:
			bugs = user.bug_set.filter(number=number)
			if bugs:
				bugs[0].delete()
	else:
		bugs = request.session.get('bugs', [])
		for bug_number in bug_selected:
			for bug in bugs:
				if bug == bug_number:
					request.session['bugs'].remove(bug_number)

# Package page
def package(request, package_name):
	"""
	Render a package page as plain HTML or as json info handy for AJAX.
	"""
	user = request.user
	queries = SoapQueries()

	bugs = queries.get_packages_bugs(package_name)
	bugs.sort(reverse=True)
	bug_list = queries.get_bugs_status(bugs)

	# Check if it's AJAX or HTML
	if request.GET.has_key('xhr'):
		return HttpResponse(simplejson.dumps({'package': package_name,
											  'bug_list': bug_list}),
							mimetype='application/javascript' )
	else:
		return render_to_response('package.html', 
								  {'package': package_name,
								   'bug_list': bug_list, 
								   'current_user': user}
								 )

