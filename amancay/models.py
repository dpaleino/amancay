# vim: set sw=4 ts=4 sts=4 noet:

from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
	user = models.ForeignKey(User)
	package_name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.package_name

class Bug(models.Model):
	user = models.ForeignKey(User)
	number = models.IntegerField()

	def __unicode__(self):
		return str(self.number)

class EmailItem(models.Model):
	user = models.ForeignKey(User)
	address = models.CharField(max_length=255)

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.address

class MaintainerEmail(EmailItem):
	pass

class SubmitterEmail(EmailItem):
	pass

class UserEmail(EmailItem):
	pass

# Pending messages, to be sent when address is validated
class Pending_Messages(models.Model):
	from_address = models.CharField(max_length=255)
	to_address = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	comment = models.TextField()
	digest = models.CharField(max_length=255)
