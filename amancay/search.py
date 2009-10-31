# vim: set sw=4 ts=4 sts=4 noet:
import time
import threading

from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext

from amancay.btsqueries import SoapQueries
from amancay.tables import _set_fav_pkgs

from django.http import HttpResponse
from django.utils import simplejson

import urllib2
import re

severities = {
    'critical': 7,
    'grave': 6,
    'serious': 5,
    'important': 4,
    'normal': 3,
    'minor': 2,
    'wishlist': 1
}

PER_PAGE = 20
def search(request):
    """
    View: render the bug table resulting from the current search.
    """
    package = request.GET.get('query')
    bug_list = []
    page = None
    info = None

    if package:
        queries = SoapQueries()
        bugs = queries.get_all_packages_bugs(package)
        bugs.sort(reverse=True)

        # We use the django Paginator to divide objects in pages but note that
        # the actual results are passed to the template as a separate list.
        # This is because we would be wasting bandwidth in requesting all the
        # objects again and again, only to feed them to the paginator and use its
        # object_list property.
        paginator = Paginator(bugs, PER_PAGE)

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)

        bug_list = queries.get_bugs_status(page.object_list)

        def severitysort(a, b):
            """Sort by severity and then by modify date"""
            d = severities[b['severity']] - severities[a['severity']]
            if d:
                return d
            return b['last_modified'] - a['last_modified']
        bug_list.sort(severitysort)

        _set_fav_pkgs(request, bug_list)

        if not bug_list:
            info = 'No results found for your search, please try again'
    else:
        info = 'Enter a package name to search for (will connect to full text'\
                ' search soon)'

    return render_to_response('search.html',
                              {'bug_list': bug_list,
                               'query': package,
                               'info_to_user': info,
                               'page': page,
                               'title': 'Latest bugs in %s' % package},
                              context_instance=RequestContext(request))


PER_PAGE = 20
def advsearch(request):
    """
    View: render the bug table resulting from the current search.
    """
    package = request.GET.get('query')
    rt1 = request.GET.get('rt1')
    rt2 = request.GET.get('rt2')
    rt3 = request.GET.get('rt3')

    print rt1, rt2, rt3

    bug_list = []
    page = None
    info = None

    if package:
        queries = SoapQueries()
        bugs = queries.get_all_packages_bugs(package)
        bugs.sort(reverse=True)

        # We use the django Paginator to divide objects in pages but note that
        # the actual results are passed to the template as a separate list.
        # This is because we would be wasting bandwidth in requesting all the
        # objects again and again, only to feed them to the paginator and use its
        # object_list property.
        paginator = Paginator(bugs, PER_PAGE)

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)

        bug_list = queries.get_bugs_status(page.object_list)

        def severitysort(a, b):
            """Sort by severity and then by modify date"""
            d = severities[b['severity']] - severities[a['severity']]
            if d:
                return d
            return b['last_modified'] - a['last_modified']
        bug_list.sort(severitysort)

        _set_fav_pkgs(request, bug_list)

        if not bug_list:
            info = 'No results found for your search, please try again'
    else:
        info = 'Enter a package name to search for (will connect to full text'\
                ' search soon)'

    return render_to_response('advsearch.html',
                              {'bug_list': bug_list,
                               'query': package,
                               'info_to_user': info,
                               'page': page,
                               'title': 'Latest bugs in %s' % package},
                              context_instance=RequestContext(request))

def checkpkgname(request):
    """
    View: check if a package exists.
    """
    pkgname = request.GET.get('pkgname')
    try:
        assert re.match("^[a-z0-9\-\+]+$", pkgname)
        v = urllib2.urlopen("http://dde.debian.net/dde/q/udd/packages/all/" + pkgname + "?t=json").read()
        u = simplejson.loads(v)
    except Exception, e:
        return HttpResponse(simplejson.dumps({'exists': 0}))
    exists = 1 if u['r'] else 0
    return HttpResponse(simplejson.dumps({'exists': exists}))


def store_search(request, search_id, bug_list, append=False, last_page=0, total=0):
    """
    Stores a search into the search db, which is serving now as a preloader.
    """
    searches = request.session.get('searches')

    if searches is None:
        request.session['searches'] = {}
        searches = request.session['searches']

    if search_id not in searches:
        searches[search_id] = {}
    searches[search_id]['stamp'] = time.time()
    searches[search_id]['last_page'] = last_page

    if total:
        searches[search_id]['total'] = total

    if append:
        if 'bugs' not in searches[search_id]:
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
        if search_id in searches:
            if (time.time() - searches[search_id]['stamp']) < 900:
                start = page * amount
                searches[search_id]['last_page'] = 0

                return searches[search_id]['bugs'][start:start+amount]

    return None


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
