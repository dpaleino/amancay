# vim: set sw=4 ts=4 sts=4 noet:
from django import template

register = template.Library()

def toolbox_widget(context):
	"""
	Render the toolbox widget.
	"""
	toolbox = {}
	title = item_type = item_list = None
	
	request = context.get('request', None)

	# Fill the info according to the type of toolbox needed
	if request.path.find('submitted_bugs') != -1:
		title = 'Submitter emails'
		item_type = 'submitter'

		if request.user.is_authenticated():
			email_list = request.user.submitteremail_set.all()
			item_list = [e.address for e in email_list]
		else:
			item_list = request.session.get('submitteremail_set')
	
	# Received bugs
	elif request.path.find('received_bugs') != -1:
		title = 'Maintainer emails'
		item_type = 'maintainer'

		if request.user.is_authenticated():
			email_list = request.user.maintaineremail_set.all()
			item_list = [e.address for e in email_list]
		else:
			item_list = request.session.get('maintaineremail_set')
	
	# Selected Packages
	elif request.path.find('package_bugs') != -1:
		title = 'Selected Packages'
		item_type = 'package'

		if request.user.is_authenticated():
			package_list = request.user.package_set.all()
			item_list = [p.package_name for p in package_list]
		else:
			item_list = request.session.get('package_set')

	# Selected bugs
	elif request.path.find('selected_bugs') != -1:
		title = 'Selected Bugs'
		item_type = 'bug'

		if request.user.is_authenticated():
			bug_list = request.user.bug_set.all()
			item_list = [b.number for b in bug_list]
		else:
			item_list = request.session.get('bug_set')
	
	# Tagged bugs
	elif request.path.find('tagged_bugs') != -1:
		title = 'User emails'
		item_type = 'user'

		if request.user.is_authenticated():
			email_list = request.user.useremail_set.all()
			item_list = [e.address for e in email_list]
		else:
			item_list = request.session.get('useremail_set')

	toolbox['title'] = title
	toolbox['item_type'] = item_type
	toolbox['item_list'] = item_list

	return {
		'toolbox':		toolbox,
		}

register.inclusion_tag('toolbox.html',
						takes_context=True)(toolbox_widget)
