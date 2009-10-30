# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from amancay.btsqueries import SoapQueries

severities = {
    'critical': 7, 
    'grave': 6, 
    'serious': 5, 
    'important': 4, 
    'normal': 3, 
    'minor': 2, 
    'wishlist': 1
}

def index(request):
    """
    Our pretty useless index page.
    """

    return render_to_response('advsearch.html', {},
                              context_instance=RequestContext(request))

def package(request, package_name):
    """
    Individual package page.
    """
    user = request.user
    queries = SoapQueries()

    bugs = queries.get_packages_bugs(package_name)
    #bugs.sort(reverse=True)
    bug_list = queries.get_bugs_status(bugs)

    def severitysort(a, b):
        """Sort by severity and then by modify date"""
        d = severities[b['severity']] - severities[a['severity']]
        if d:
            return d
        return b['last_modified'] - a['last_modified']
    bug_list.sort(severitysort) 
    
    # Check if it's AJAX or HTML
    if 'xhr' in request.GET:
        return HttpResponse(simplejson.dumps({"package": package_name,
                                              "bug_list": bug_list}),
                            mimetype='application/javascript')
    else:
        return render_to_response('package.html',
                                  {'package': package_name,
                                   'bug_list': bug_list},
                                  context_instance=RequestContext(request))
