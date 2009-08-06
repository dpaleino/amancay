# vim: set sw=4 ts=4 sts=4 noet:
from django.http import HttpResponse

def add_package(request):
	"""
	Add a package to our session watched list.
	"""
	user = request.user
	package_name = request.GET['id']

	if user.is_authenticated():
		packages = user.package_set.filter(package_name=package_name)
		if not packages:
			user.package_set.create(package_name=package_name)
			return HttpResponse(status=200)
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
		packages = request.session.get('packages', [])
		if package_name in packages:
			request.session['packages'].remove(package_name)
			return HttpResponse(status=500)
