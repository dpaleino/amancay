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
from bts_queries import soap_queries, bug_sort
queries = soap_queries()

# Needed for timestamps, page calculation
import time, math

# Manage the sessions myself
from django.contrib.sessions.models import Session

# Bug views
def search(request):
	user = request.user
	bugs = []
	package = request.GET.get('package_search')
	amount = 20

	# Get the page
	page = request.GET.get('page')
	try:
		page = int(page)
		page -= 1
	except:
		page=0

	# Perform the query
	if (package):
		search_id = "package:%s" % package
		bug_list = retrieve_search(request, search_id, amount, page)
		if (bug_list == None):
			bugs = queries.get_all_packages_bugs(package)
			bugs.sort(reverse=True)
			bug_list = get_bugs_status(request, search_id, bugs, amount, page)
			total = len(bugs)
		else:
			total = request.session["searches"][search_id]["total"]
		pages = int(math.ceil(total/(amount*1.0)))
		return render_bug_table(request, "Latest bugs for %s" % package, 
			bug_list, page+1, pages, total, "package_search")
	else:
		return render_bug_table(request, "", None, 0, 0, 0, "search")

def get_bugs_status(request, search_id, bugs, amount, page):
	if (bugs != None and len(bugs) > 0):
		start=page*amount
		bug_list = queries.get_bugs_status(bugs[start:start+amount])
		store_search(request, search_id, bug_list, total=len(bugs))	
		bug_list.sort(bug_sort.cmp_log_modified, reverse=True)

		# Start the read-ahead thread
		reader = read_ahead(request, search_id, bugs, amount)
		reader.start()
	else:
		bug_list = None
	return bug_list

def store_search(request, search_id, bug_list, append=False, last_page=0,
					total=0):
	searches = request.session.get("searches")
	if (searches == None):
		request.session["searches"] = {}
		searches = request.session["searches"]
	if (not searches.has_key(search_id)):
		searches[search_id] = {}
	searches[search_id]["stamp"] = time.time()
	searches[search_id]["last_page"] = last_page
	if (total > 0):
		searches[search_id]["total"] = total
	if (append):
		if (not searches[search_id].has_key("bugs")):
			searches[search_id]["bugs"] = []
	else:
		searches[search_id]["bugs"] = []
	searches[search_id]["bugs"].extend(bug_list)

def retrieve_search(request, search_id, amount, page=0):
	searches = request.session.get("searches")
	if (searches != None):
		if (searches.has_key(search_id)):
			if (time.time() - searches[search_id]["stamp"] < 900):
				start = page * amount
				searches[search_id]["last_page"] = 0
				return searches[search_id]["bugs"][start:start+amount]
	return None

# Bug renderer.
def render_bug_table(request, title, bug_list, page, num_pages, total,
					current_view):
	
	# Calculate the pages
	start = page - 5
	if (start < 1): start = 1
	end = page + 5
	if (end >= num_pages): end = num_pages - 1
	pages = range(start, end)

	# URL for future searches
	url = "%s?%s=%s" % (request.path, current_view,
		request.GET.get(current_view))

	if (request.GET.has_key('xhr')):
		# We only need to list the data.
		return HttpResponse( simplejson.dumps(bug_list),
		                     mimetype='application/javascript' )
	elif (request.path.find("table") != -1):
		# We only need to render the table
		return render_to_response('table.html', 
		                          {'bug_list': bug_list,
								   'current_view': current_view,
								   'url': url,
								   'total_bugs': total,
								   'current_page': page,
								   'pages': pages},
		                         )
	else:
		# We need to render the whole page
		return render_to_response('search.html', 
		                          {'bug_list': bug_list,
								   'current_view': current_view,
								   'url': url,
								   'total_bugs': total,
								   'current_user': request.user,
								   'current_page': page,
								   'pages': pages},
		                         )



# Read Ahead class
import threading
class read_ahead (threading.Thread):
	def __init__(self, request, search_id, bugs, amount):
		threading.Thread.__init__(self)
		self.request = request
		self.bugs = bugs
		self.amount = amount
		self.search_id = search_id
	def run(self):
		start = self.amount
		old_session = Session.objects.get(pk=self.request.session.session_key)
		while (start < len(self.bugs)):
			bug_list = queries.get_bugs_status(self.bugs[start:start+self.amount])
			store_search(self.request, self.search_id, bug_list, True)	
			start += self.amount
			# Ugly hack to make the session save
			Session.objects.save(self.request.session.session_key, 
				self.request.session._session, old_session.expire_date)


