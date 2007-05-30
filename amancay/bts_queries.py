#!/usr/bin/python

# Abstract class that states the bts_queries all implementing classes
# should support
class bts_queries:
	
	# Returns an array with the status for all bug_numbers received.
	def get_bugs_status(self, bug_numbers):
		pass

	# Returns an array of bug numbers, for all received packages.
	def get_packages_bugs(self, packages):
		pass
	
	# Returns an array of bug numbers, for which the emails received are
	# submitters.
	def get_submitters_bugs(self, emails):
		pass
	
	# Returns an array of bug numbers, for which the emails received are
	# maintainers.
	def get_maintainers_bugs(self, emails):
		pass



# ************************ SOAP Queries *****************************

import SOAPpy 
# Uncomment those to enable debugging
#server.config.dumpSOAPOut = 1
#server.config.dumpSOAPIn = 1

class soap_queries(bts_queries):
	def __init__(self):
		self.url = 'http://bugs.donarmstrong.com/cgi-bin/soap.cgi'
		self.ns = 'Debbugs/SOAP'
		self.server = SOAPpy.SOAPProxy(self.url, self.ns)

	def process_result(self, result):
		if type(result.item) == type([]):
			return [ item.value for item in result.item ]
		else:
			return [ result.item.value ]

	def get_bugs_status(self, bug_numbers):
		self.server.soapaction = '%s#get_status' % self.ns
		result = self.server.get_status(bug_numbers)
		return self.process_result(result)
	
	def get_packages_bugs(self, packages):
		self.server.soapaction = '%s#get_bugs' % self.ns
		result = self.server.get_bugs("package",packages)
		return result
	
	def get_submitters_bugs(self, emails):
		self.server.soapaction = '%s#get_bugs' % self.ns
		result = self.server.get_bugs("submitter", emails)
		return result
	
	def get_maintainers_bugs(self, emails):
		self.server.soapaction = '%s#get_bugs' % self.ns
		result = self.server.get_bugs("maint",emails)
		return result

# ************************ LDAP Queries *****************************




