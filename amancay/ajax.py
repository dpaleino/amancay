# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse

from amancay.bugs import handle_email

def _add_item(request, item_type, new_item):
	"""
	Add the given item to either the session or user set.
	"""
	item_set = '%s_set' % item_type

	if request.user.is_authenticated():
		item_set = getattr(request.user, item_set)
		items = item_set.filter(**new_item)

		if items:
			return False
		else:
			item_set.create(**new_item)
			return True
	else:
		items = request.session.get(item_set, [])
		new_item = new_item.values()[0]

		if new_item in items:
			return False
		else:
			items.append(new_item)
			request.session[item_set] = items
			return True

def _remove_item(request, item_type, remove_item):
	"""
	Remove the given item from either the session or user set.
	"""
	item_set = '%s_set' % item_type

	if request.user.is_authenticated():
		item_set = getattr(request.user, item_set)
		items = item_set.filter(**remove_item)

		if items:
			items[0].delete()
			return True
		else:
			return False
	else:
		items = request.session.get(item_set, [])
		remove_value = remove_item.values()[0]

		if remove_value in items:
			items.remove(remove_value)
			request.session[item_set] = items
			return True
		else:
			return False

def _get_post_or_get(request, item):
	item = request.GET.get(item, None)

	if not item:
		item = request.POST.get(item, None)

	return item

def package_add(request):
	"""
	Add a package to our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _add_item(request, 'package', {'package_name': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def package_remove(request):
	"""
	Remove a package from the watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _remove_item(request, 'package', {'package_name': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def bug_add(request):
	"""
	Add a bug to our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _add_item(request, 'bug', {'number': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def bug_remove(request):
	"""
	Remove a bug from the watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _remove_item(request, 'bug', {'number': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def maintainer_add(request):
	"""
	Add a maintainer to our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _add_item(request, 'maintaineremail', {'address': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def maintainer_remove(request):
	"""
	Remove a maintainer from our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _remove_item(request, 'maintaineremail', {'address': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def submitter_add(request):
	"""
	Add a submitter/user to our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _add_item(request, 'submitteremail', {'address': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def submitter_remove(request):
	"""
	Remove a submitter/user from our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _remove_item(request, 'submitteremail', {'address': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def user_add(request):
	"""
	Add a submitter/user to our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _add_item(request, 'useremail', {'address': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def user_remove(request):
	"""
	Remove a submitter/user from our watched list.
	"""
	item = _get_post_or_get(request, 'id')

	if _remove_item(request, 'useremail', {'address': item}):
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def _bug_toggle_subscribe(request, subscribe=True):
	"""
	Toggle subscription to a specific bug report.
	"""
	bug_number = request.GET['id']

	if subscribe:
		action = 'subscribe'
	else:
		action = 'unsubscribe'

	if request.user.is_authenticated():
		to_address = ['%s-%s@bugs.debian.org' % (bug_number, action)]

		# FIXME: this never tells us if the email left the building
		handle_email(request, to_address, '', '')
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def bug_subscribe(request):
	"""
	Subscribe to a specific bug report.
	"""
	return _bug_toggle_subscribe(request, subscribe=True)

def bug_unsubscribe(request):
	"""
	Unsubscribe to a specific bug report.
	"""
	return _bug_toggle_subscribe(request, subscribe=False)
