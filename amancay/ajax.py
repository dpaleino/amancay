# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse
from amancay.bugs import handle_email

def add_package(request):
	"""
	Add a package to our session watched list.
	"""
	user = request.user
	package_name = request.GET['id']

	if user.is_authenticated():
		packages = user.package_set.filter(package_name=package_name)[:1]
		if not packages:
			user.package_set.create(package_name=package_name)
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=500)
	else:
		packages = request.session.get('packages', [])
		if package_name in packages:
			return HttpResponse(status=500)
		else:
			request.session['packages'].append(package_name)
			return HttpResponse(status=200)

def remove_package(request):
	"""
	Remove a package from the watched list.
	"""
	user = request.user
	package_name = request.GET['id']

	if user.is_authenticated():
		packages = user.package_set.filter(package_name=package_name)[:1]
		if packages:
			packages[0].delete()
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=500)
	else:
		packages = request.session.get('packages', [])
		if package_name in packages:
			request.session['packages'].remove(package_name)
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=500)

def _bug_toggle_subscribe(request, subscribe=True):
	"""
	Toggle subscription to a specific bug report
	"""
	user = request.user
	bug_number = request.GET['id']

	if subscribe:
		action = 'subscribe'
	else:
		action = 'unsubscribe'

	if user.is_authenticated():
		subscribe_email = request.user.email
		to_address = ['%s-%s@bugs.debian.org' % (bug_number, action)]

		# FIXME: this never tells us if the email left the building
		handle_email(request, to_address, '', '')
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=500)

def bug_subscribe(request):
	"""
	Subscribe to a specific bug report
	"""
	return _bug_toggle_subscribe(request, subscribe=True)

def bug_unsubscribe(request):
	"""
	Unsubscribe to a specific bug report
	"""
	return _bug_toggle_subscribe(request, subscribe=False)