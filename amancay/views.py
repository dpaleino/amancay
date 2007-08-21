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

# Tables POST processing
from tables import process_post, selected_bugs
from search import search

# The index page doesn't really do much.
def index(request):
	item_list = process_post(request)
	# Check if it's AJAX or HTML
	if (request.GET.has_key('xhr')):
		return HttpResponse( simplejson.dumps({"item_list":	item_list}),
		                     mimetype='application/javascript' )
	else:
		# TODO: choose which view to show.
		return search(request)


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

# The bug page uses regular expresions to parse the log
import re
# The bug page uses rfc822 to parse emails, dates, etc.
import email.Utils
import email.Header

def bug(request, bug_number):

	# Process post
	info = add_comment(request, bug_number)

	user = request.user
	queries = soap_queries()
	bug_status = queries.get_bugs_status(bug_number)[0]
	bug_originator = email.Utils.parseaddr(bug_status["originator"])
	bug_log = queries.get_bug_log(bug_number)

	# Regular expressions to parse the mails
	from_re = re.compile('^From: ?(.+)$', re.MULTILINE)
	subject_re = re.compile('^Subject: ?(.+)$', re.MULTILINE)
	date_re = re.compile('^Date: ?(.+)$', re.MULTILINE)

	bug_messages = []
	for item in bug_log:
		message = {}
		# Parse the header
		from_value = from_re.findall(item["header"])
		subject_value = subject_re.findall(item["header"])
		date_value = date_re.findall(item["header"])
		# Filter the values
		if (len(from_value) > 0):
			e_from = email.Utils.parseaddr(from_value[0])
			d_from = email.Header.decode_header(e_from[0])
			if (d_from[0][1] != None):
				message["from"] = [d_from[0][0].decode(d_from[0][1]), e_from[1]]
			else:
				message["from"] = [e_from[0], e_from[1]]
			if (message["from"][0] == "" and message["from"][1] != ""):
				message["from"][0] = message["from"][1]

		if (len(subject_value) > 0):
			message["subject"] = subject_value[0]
		if (len(date_value) > 0):
			message["date"] = email.Utils.mktime_tz(email.Utils.parsedate_tz(
			                                         date_value[0]))
	
		# Get the body
		message["body"] = item["body"]
		bug_messages.append(message)

	return render_to_response('bug.html', 
	                          {'bug_number': bug_number,
							   'info_to_user': info,
							   'bug_originator': bug_originator,
							   'bug_status': bug_status,
	                           'bug_messages': bug_messages,
	                           'current_user': user}
	                         )

# Function to add a comment to bug
def add_comment(request, bug_number):
	user = request.user
	subject = request.POST.get("subject")
	comment = request.POST.get("comment")
	if (subject and comment):
		to_address = "%s@bugs.debian.org" % bug_number
		# If the user is registered, we send the mail.  If not, we store it, and
		# validate the email
		if (user.is_authenticated()):
			from django.core.mail import send_mail
			send_mail(subject, comment, user.email, [to_address])
			return "Your comment has been successfully sent"
		else:
			# TODO
			return "A mail has been sent to your address to validate it"
	else:
		if (subject or comment):
			return "You need to enter both the subject and the comment"
		else:
			return None

