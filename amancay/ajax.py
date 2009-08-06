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
	else:
		packages = request.session.get('packages', [])
		for package in packages:
			if package == package_name:
				return 
		request.session['packages'].append(package_name)

	return HttpResponse(status=200)
