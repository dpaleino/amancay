# vim: set sw=4 ts=4 sts=4 noet:
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext

from amancay.btsqueries import SoapQueries

def _set_fav_pkgs(request, bug_list):
    """
    In a bug list, set if the packages are considered favourites (in place).
    """
    if request.user.is_authenticated():
        package_list = [p.package_name for p in request.user.package_set.all()]
    else:
        package_list = request.session.get('package_set', [])

    for bug in bug_list:
        if bug.package in package_list:
            bug.pkg_fav = True
        else:
            bug.pkg_fav = False

# FIXME: must be taken from prefs
PER_PAGE = 10
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
            user_emails = request.session.get('maintaineremail_set', [])

        bugs = queries.get_maintainers_bugs(user_emails)

    elif view == 'submitted_bugs':
        if request.user.is_authenticated():
            submitter_emails = [e.address for e in request.user.submitteremail_set.all()]
        else:
            submitter_emails = request.session.get('submitteremail_set', [])

        bugs = queries.get_submitters_bugs(submitter_emails)

    elif view == 'selected_bugs':
        if request.user.is_authenticated():
            bugs = [b.number for b in request.user.bug_set.all()]
        else:
            bugs = request.session.get('bug_set', [])

    elif view == 'package_bugs':
        if request.user.is_authenticated():
            package_list = [p.package_name for p in request.user.package_set.all()]
        else:
            package_list = request.session.get('package_set', [])

        bugs = queries.get_packages_bugs(package_list)

    elif view == 'tagged_bugs':
        if request.user.is_authenticated():
            user_emails = [e.address for e in request.user.useremail_set.all()]
        else:
            user_emails = request.session.get('useremail_set', [])

        bugs = queries.get_tagged_bugs(user_emails)

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

    bugs = page.object_list
    if bugs:
        bug_list = queries.get_bugs_status(bugs)
        bug_list.sort(key=lambda x: x.package)

    return {'bug_list': bug_list,
            'current_view': view,
            'page': page}

def received_bugs(request):
    """
    Render a table view for bugs we have received as maintainers.
    """
    data_dict = _get_bug_list(request, 'received_bugs')
    data_dict['title'] = 'Latest received bugs'

    return render_to_response('table.html',
                              data_dict,
                              context_instance=RequestContext(request))

def submitted_bugs(request):
    """
    Render a table view for bugs we have submitted ourselves.
    """
    data_dict = _get_bug_list(request, 'submitted_bugs')
    data_dict['title'] = 'Latest submitted bugs'

    _set_fav_pkgs(request, data_dict['bug_list'])

    return render_to_response('table.html',
                              data_dict,
                              context_instance=RequestContext(request))

def selected_bugs(request):
    """
    Render a table view for bugs we are watching.
    """
    data_dict = _get_bug_list(request, 'selected_bugs')
    data_dict['title'] = 'Latest selected bugs'

    _set_fav_pkgs(request, data_dict['bug_list'])

    return render_to_response('table.html',
                              data_dict,
                              context_instance=RequestContext(request))

def package_bugs(request):
    """
    Render a table view for our watched packages.
    """
    data_dict = _get_bug_list(request, 'package_bugs')
    data_dict['title'] = 'Latest bugs on selected packages'

    _set_fav_pkgs(request, data_dict['bug_list'])

    return render_to_response('table.html',
                              data_dict,
                              context_instance=RequestContext(request))

def tagged_bugs(request):
    """
    Render a table view for bugs we have tagged.
    """
    data_dict = _get_bug_list(request, 'tagged_bugs')
    data_dict['title'] = 'Latest tagged bugs'

    # TODO: fix this, bugs is a dict where every value is a dict of tags and
    # bugs associated to one mail
    return render_to_response('table.html',
                              data_dict,
                              context_instance=RequestContext(request))
