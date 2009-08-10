# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from amancay.bts_queries import SoapQueries
queries = SoapQueries()

# Bug renderer.
def render_bug_table(request, queries, title, bugs, amount, current_view):
	if bugs:
		bug_list = queries.get_bugs_status(bugs[:amount])
		bug_list.sort(key=lambda x: x.package)
	else:
		bug_list = None

	if request.user.is_authenticated():
		fav_packages = [p.package_name for p in request.user.package_set.all()]

		for bug in bug_list:
			if bug.package in fav_packages:
				bug.pkg_fav = True
			else:
				bug.pkg_fav = False

	if request.GET.has_key('xhr'):
		# We only need to list the data.
		return HttpResponse(simplejson.dumps(bug_list),
							 mimetype='application/javascript')
	elif request.path.find("table") != -1:
		# We only need to render the table
		return render_to_response('table.html', 
								  {'bug_list': bug_list,
								   'table_title': title,
								   'current_view': current_view},
								  context_instance=RequestContext(request))
	else:
		return render_to_response('index.html', 
								  {'bug_list': bug_list,
								   'table_title': title,
								   'current_view': current_view},
								  context_instance=RequestContext(request))

# Bug views
def submitted_bugs(request):
	process_post(request)
	user = request.user
	bugs = []
	if (user.is_authenticated()):
		emails = user.submitteremail_set.all()
		submitter_emails = [ str(e) for e in emails]
	else:
		submitter_emails = request.session.get('submitter_emails')
	if (submitter_emails):
		bugs = queries.get_submitters_bugs(submitter_emails)
		bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest submitted bugs",
	bugs, 15, "submitted_bugs")

def received_bugs(request):
	process_post(request)
	user = request.user
	bugs = []
	if (user.is_authenticated()):
		emails = user.maintaineremail_set.all()
		maintainer_emails = [str(e) for e in emails]
	else:
		maintainer_emails = request.session.get('maintainer_emails')
	if (maintainer_emails):
		bugs = queries.get_maintainers_bugs(maintainer_emails)
	bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest received bugs", bugs,
	15, "received_bugs")
		
def package_bugs(request):
	process_post(request)
	user = request.user
	bugs = []

	if user.is_authenticated():
		package_list = request.user.package_set.all()
		package_list = [p.package_name for p in package_list]
	else:
		package_list = request.session.get('packages')

	if package_list:
		bugs = queries.get_packages_bugs(package_list)
		bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest bugs on selected packages", bugs, 15, "package_bugs")

def selected_bugs(request):
	process_post(request)
	user = request.user
	if (user.is_authenticated()):
		bugs = [b.number for b in request.user.bug_set.all()]
	else:
		bugs = request.session.get('bugs')
	if (bugs != None):
		bugs.sort(reverse=True)
	return render_bug_table(request, queries, "Latest selected bugs", bugs,
	15, "selected_bugs")

def tagged_bugs(request):
	process_post(request)
	user = request.user
	if (user.is_authenticated()):
		emails = user.useremail_set.all()
		user_emails = [ str(e) for e in emails]
	else:
		user_emails = request.session.get('user_emails')
	bugs = {}
	if (user_emails):
		bugs = queries.get_tagged_bugs(user_emails)
	print bugs
	# bugs.sort(reverse=True)
	# TODO: fix this, bugs is a dict where every value is a dict of tags and
	# bugs associated to one mail
	bugs = []
	return render_bug_table(request, queries, "Latest received bugs", bugs,
	15, "received_bugs")


# Simple method that just calls the appropiate function.
def process_post(request):
	if request.POST:
		# Packages
		if (request.POST.has_key('package')):
			return add_package(request)
		elif (request.POST.has_key('package_select')):
			return remove_packages(request)
		# Bugs
		elif (request.POST.has_key('bug')):
			return add_bug(request)
		elif (request.POST.has_key('bug_select')):
			return remove_bugs(request)
		# Submitter Emails
		elif (request.POST.has_key('submitter_email')):
			return add_submitter_email(request)
		elif (request.POST.has_key('submitter_email_select')):
			return remove_submitter_emails(request)
		# Maintainer Emails
		elif (request.POST.has_key('maintainer_email')):
			return add_maintainer_email(request)
		elif (request.POST.has_key('maintainer_email_select')):
			return remove_maintainer_emails(request)
		# User Emails
		elif (request.POST.has_key('user_email')):
			return add_user_email(request)
		elif (request.POST.has_key('user_email_select')):
			return remove_user_emails(request)
	return []

# Data processing
def add_item(request, item_set, item_record, session_name):
	if (item_set != None):
		items = item_set.filter(**item_record)
		if (len(items) == 0):
			item_set.create(**item_record)
		return [ str(i) for i in item_set.all() ]
	else:
		items = request.session.get(session_name)
		if (items == None):
			items = request.session[session_name] = []
		item_value = item_record.values()[0]
		for item in items:
			if (item == item_value):
				return items
		items.append(item_value)
		return items

def add_package(request):
	user = request.user
	package_name = request.POST['package']
	item_set = None
	if (user.is_authenticated()):
		item_set = user.package_set
	return add_item(request, item_set, {"package_name":package_name},"packages")

def add_bug(request):
	user = request.user
	bug_number = request.POST['bug']
	item_set = None
	if (user.is_authenticated()):
		item_set = user.bug_set
	return add_item(request, item_set, {"number":bug_number}, "bugs")

def add_submitter_email(request):
	user = request.user
	email = request.POST['submitter_email']
	item_set = None
	if (user.is_authenticated()):
		item_set = user.submitteremail_set
	return add_item(request, item_set, {"address":email}, "submitter_emails")

def add_maintainer_email(request):
	user = request.user
	email = request.POST['maintainer_email']
	item_set = None
	if (user.is_authenticated()):
		item_set = user.maintaineremail_set
	return add_item(request, item_set, {"address":email}, "maintainer_emails")

def add_user_email(request):
	user = request.user
	email = request.POST['user_email']
	item_set = None
	if (user.is_authenticated()):
		item_set = user.useremail_set
	return add_item(request, item_set, {"address":email}, "user_emails")

def remove_items(request, selected_items, item_set, item_field, session_name):
	if (item_set != None):
		for item in selected_items:
			items = item_set.filter(**{item_field:item})
			if (len(items) != 0):
				items[0].delete()
		return [ str(i) for i in item_set.all()]
	else:
		items = request.session.get(session_name)
		if (items == None):
			items = request.session[session_name] = []
		else:
			for sel_item in selected_items:
				for item in items:
					if (item == sel_item):
						items.remove(sel_item)
		return items


def remove_packages(request):
	user = request.user
	selected = request.POST.getlist("package_select")
	item_set = None
	if (user.is_authenticated()):
		item_set = user.package_set
	return remove_items(request, selected, item_set, "package_name","packages")

def remove_bugs(request):
	user = request.user
	selected = request.POST.getlist("bug_select")
	item_set = None
	if (user.is_authenticated()):
		item_set = user.bug_set
	return remove_items(request, selected, item_set, "number","bugs")

def remove_submitter_emails(request):
	user = request.user
	selected = request.POST.getlist("submitter_email_select")
	item_set = None
	if (user.is_authenticated()):
		item_set = user.submitteremail_set
	return remove_items(request, selected, item_set, "address","submitter_emails")

def remove_maintainer_emails(request):
	user = request.user
	selected = request.POST.getlist("maintainer_email_select")
	item_set = None
	if (user.is_authenticated()):
		item_set = user.maintaineremail_set
	return remove_items(request, selected, item_set, "address","maintainer_emails")

def remove_user_emails(request):
	user = request.user
	selected = request.POST.getlist("user_email_select")
	item_set = None
	if (user.is_authenticated()):
		item_set = user.useremail_set
	return remove_items(request, selected, item_set, "address","user_emails")

