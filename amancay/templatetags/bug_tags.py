# vim: set sw=4 ts=4 sts=4 noet:

TAGS = ('patch', 'wontfix', 'moreinfo', 'unreproducible', 'help', 'pending', 'fixed', 'security', 'upstream', 'confirmed', 'fixed-upstream', 'fixed-in-experimental', 'd-i', 'ipv6', 'lfs', 'l10n', 'potato', 'woody', 'sarge', 'sarge-ignore', 'etch', 'etch-ignore', 'sid', 'experimental')

from django import template

register = template.Library()

def bug_tags_selector(context):
	"""
	Render tags checkboxes for the current bug.
	"""

	bug = context.get('bug_status')
	if bug is None:
		return None
	
	active_tags = bug.tags.split(' ')

	all_tags = [t for t in TAGS if t not in active_tags]

	# all_tags could be [''], let's check it's not
	if all_tags and all_tags[0] == '':
		all_tags = []

	print active_tags, all_tags

	return {
		'bug':			bug,
		'all_tags':		all_tags,
		'active_tags':	active_tags,
		}

register.inclusion_tag('bug_tags_selector.html',
						takes_context=True)(bug_tags_selector)
