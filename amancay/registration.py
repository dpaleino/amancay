# vim: set sw=4 ts=4 sts=4 noet:
from django import oldforms as forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def register(request):
	"""
	Render user registration form.
	"""
	form = UserCreationForm()

	if request.method == 'POST':
		data = request.POST.copy()
		errors = form.get_validation_errors(data)
		if not errors:
			new_user = form.save()
			return HttpResponseRedirect('/accounts/created/')
	else:
		data = errors = {}

	return render_to_response('registration/register.html', {
		'form' : forms.FormWrapper(form, data, errors)
	})
