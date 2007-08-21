from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):
	user = models.ForeignKey(User)
	package_name = models.CharField(maxlength=200)

	def __str__(self):
		return self.package_name

class Bug(models.Model):
	user = models.ForeignKey(User)
	number = models.IntegerField()

	def __str__(self):
		return str(self.number)

class EmailItem(models.Model):
	user = models.ForeignKey(User)
	address = models.CharField(maxlength=255)

	def __str__(self):
		return self.address

class MaintainerEmail(EmailItem):
	pass

class SubmitterEmail(EmailItem):
	pass

class UserEmail(EmailItem):
	pass

