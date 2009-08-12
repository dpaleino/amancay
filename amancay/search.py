# vim: set sw=4 ts=4 sts=4 noet:
import math
import time
import threading

from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from amancay.btsqueries import SoapQueries
queries = SoapQueries()

# Bug views
def search(request):
	"""
	View: render the bug table resulting from the current search.
	"""
	user = request.user
	amount = 20 # TODO: get this amount from user prefs

	# Get the page
	page = request.GET.get('page')
	try:
		page = int(page)
		page -= 1
	except:
		page = 0

	# Perform the query
	package = request.GET.get('package_search')
	if package:
		search_id = 'package:%s' % package
		bug_list = retrieve_search(request, search_id, amount, page)

		if bug_list is None:
			bugs = queries.get_all_packages_bugs(package)
			bugs.sort(reverse=True)
			bug_list = get_bugs_status(request, search_id, bugs, amount, page)
			total = len(bugs)
		else:
			total = request.session['searches'][search_id]['total']

		pages = int(math.ceil(total/(amount*1.0)))

		return render_bug_table(request, 'Latest bugs for %s' % package,
			bug_list, page+1, pages, total, 'package_search')
	else:
		return render_bug_table(request, '', None, 0, 0, 0, 'search')

def get_bugs_status(request, search_id, bugs, amount, page):
	"""
	Gets the status for the bugs in the provided list, returns such list.
	"""
	if bugs:
		start = page * amount
		bug_list = queries.get_bugs_status(bugs[start:start+amount])
		store_search(request, search_id, bug_list, total=len(bugs))
		bug_list.sort(key=lambda x: x.log_modified, reverse=True)

		# Start the read-ahead thread
		reader = _ReadAhead(request, search_id, bugs, amount)
		reader.start()
	else:
		bug_list = None

	return bug_list

def store_search(request, search_id, bug_list, append=False, last_page=0, total=0):
	"""
	Stores a search into the search db, which is serving now as a preloader.
	"""
	searches = request.session.get('searches')

	if searches is None:
		request.session['searches'] = {}
		searches = request.session['searches']

	if not searches.has_key(search_id):
		searches[search_id] = {}
	searches[search_id]['stamp'] = time.time()
	searches[search_id]['last_page'] = last_page

	if total:
		searches[search_id]['total'] = total

	if append:
		if not searches[search_id].has_key('bugs'):
			searches[search_id]['bugs'] = []
	else:
		searches[search_id]['bugs'] = []

	searches[search_id]['bugs'].extend(bug_list)

def retrieve_search(request, search_id, amount, page=0):
	"""
	Return a queued search.
	"""
	searches = request.session.get('searches')

	if searches is not None:
		if searches.has_key(search_id):
			if (time.time() - searches[search_id]['stamp']) < 900:
				start = page * amount
				searches[search_id]['last_page'] = 0

				return searches[search_id]['bugs'][start:start+amount]

	return None

def render_bug_table(request, title, bug_list, page, num_pages, total, current_view):
	"""
	Render an individual bug table.
	"""
	# Calculate the pages
	start = page - 5

	# FIXME: use django pager here
	if start < 1:
		start = 1
	end = page + 5

	if end > num_pages:
		end = num_pages

	pages = range(start, end+1)

	# URL for future searches
	url = 'http://%s/search/?%s=%s' % (Site.objects.get_current().domain,
									   current_view,
									   request.GET.get(current_view))

	if request.GET.has_key('xhr'):
		# We only need to list the data.
		return HttpResponse(simplejson.dumps(bug_list),
							mimetype='application/javascript')
	elif request.path.find('table') != -1:
		# We only need to render the table
		return render_to_response('table_widget.html',
								  {'bug_list': bug_list,
								   'current_view': current_view,
								   'url': url,
								   'total_bugs': total,
								   'current_page': page,
								   'pages': pages},
								  context_instance=RequestContext(request))
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
								  context_instance=RequestContext(request))

class _ReadAhead(threading.Thread):
	"""
	ReadAhead class used to preload bug lists.
	"""
	# FIXME: what does this do precisely?
	# FIXME: what about a cache?
	def __init__(self, request, search_id, bugs, amount):
		threading.Thread.__init__(self)
		self.request = request
		self.bugs = bugs
		self.amount = amount
		self.search_id = search_id

	def run(self):
		"""
		Start the ReadAhead thread.
		"""
		start = self.amount
		old_session = Session.objects.get(pk=self.request.session.session_key)
		bug_number = len(self.bugs)
		while start < bug_number:
			bug_list = queries.get_bugs_status(self.bugs[start:start+self.amount])
			store_search(self.request, self.search_id, bug_list, True)
			start += self.amount
			# FIXME: Ugly hack to make the session save
			Session.objects.save(self.request.session.session_key,
								 self.request.session._session,
								 old_session.expire_date)
