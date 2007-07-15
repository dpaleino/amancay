from django import template

register = template.Library()

def tstodate(value, arg=None):
	from datetime import datetime
	if not value:
		return ''
	try:
		value=float(value)
	except:
		return ''
	if arg is None:
		arg = "%s"
	return datetime.strftime(datetime.fromtimestamp(value),arg)

register.filter(tstodate)
