# vim: set sw=4 ts=4 sts=4 noet:
import SOAPpy

class BtsQueries:
	"""
	Abstract class implementing stubs for the required BTS queries the
	different implementations should support.

	"""
	def get_bugs_status(self, bug_numbers):
		"""
		Returns an array with the status for all bug_numbers received.
		"""
		pass

	def get_packages_bugs(self, packages):
		"""
		Returns an array of bug numbers, for all received packages.
		"""
		pass

	def get_submitters_bugs(self, emails):
		"""
		Returns an array of bug numbers, for which the emails received are
		submitters.
		"""
		pass

	def get_maintainers_bugs(self, emails):
		"""
		Returns an array of bug numbers, for which the emails received are
		maintainers.
		"""
		pass

# ************************ SOAP Queries *****************************
# Uncomment those to enable debugging
#server.config.dumpSOAPOut = 1
#server.config.dumpSOAPIn = 1

class SoapQueries(BtsQueries):
	"""
	SOAP based BtsQueries class.
	"""
	def __init__(self):
		self.url = 'http://bugs.debian.org/cgi-bin/soap.cgi'
		#self.url = 'http://bugs.donarmstrong.com/cgi-bin/soap.cgi'
		self.ns = 'Debbugs/SOAP'
		self.server = SOAPpy.SOAPProxy(self.url, self.ns)

	def __process_result(self, result):
		if isinstance(result.item, list):
			return [item.value for item in result.item]
		else:
			return [result.item.value]

	def get_bugs_status(self, bug_numbers):
		result = self.server.get_status(bug_numbers)
		return self.__process_result(result)

	def get_packages_bugs(self, packages):
		result = self.server.get_bugs('package', packages)
		return result

	def get_submitters_bugs(self, emails):
		result = self.server.get_bugs('submitter', emails)
		return result

	def get_maintainers_bugs(self, emails):
		result = self.server.get_bugs('maint', emails)
		return result

	def get_all_packages_bugs(self, packages):
		# FIXME: Not in BtsQueries
		pkg = self.server.get_bugs('package', packages)
		src = self.server.get_bugs('src', packages)
		result = pkg + src
		return list(result)

	def get_bug_log(self, bug):
		# FIXME: Not in BtsQueries
		result = self.server.get_bug_log(bug)
		return result

	def get_tagged_bugs(self, users):
		# FIXME: Not in BtsQueries
		# TODO: ask Don to allow many users at the same time
		result = {}
		for user in users:
			result[user] = self.server.get_usertag(user)
		return result
