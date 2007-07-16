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

register.filter(tstodate)
