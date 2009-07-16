from datetime import datetime
from django import template

register = template.Library()

def tstodate(value, arg=None):
	"""
	Convert a timestamp into a human readable date.
	"""
	if not value:
		return ''
	try:
		value=float(value)
	except:
		return ''
	if arg is None:
		d = datetime.fromtimestamp(value)
		now = datetime.now()
		if (d.year != now.year):
			# marga says:
			return d.strftime("%d/%m/%y")
		elif (d.month != now.month or d.day != now.day):
			return d.strftime("%b %e")
		#elif (d.month != now.month):
		#	return d.strftime("%b %e")
		#elif (d.day != now.day):
		#	return d.strftime("%a %e")
		else:
			return d.strftime("%k:%M")
	
	return datetime.fromtimestamp(value).strftime(arg)

def tstodatetime(value, arg=None):
	"""
	Convert a timestamp into a datetime object.
	"""
	if not value:
		return ''
	try:
		value=float(value)
	except:
		return ''

	d = datetime.fromtimestamp(value)

	return d

register.filter(tstodate)
register.filter(tstodatetime)
