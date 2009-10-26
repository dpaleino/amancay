# vim: set sw=4 ts=4 sts=4 noet:
import SOAPpy
from time import time

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

class SoapQueries(BtsQueries):
    """
    SOAP based BtsQueries class.
    """
    def __init__(self):
        #self.url = 'http://bugs.debian.org/cgi-bin/soap.cgi'
        self.url = 'http://bugs-rietz.debian.org/cgi-bin/soap.cgi'
        #self.url = 'http://bugs.donarmstrong.com/cgi-bin/soap.cgi'
        self.ns = 'Debbugs/SOAP'
        self.server = SOAPpy.SOAPProxy(self.url, self.ns)
        #self.server.config.dumpSOAPOut = 1  # Uncomment those to enable debugging
        #self.server.config.dumpSOAPIn = 1

    def get_bugs_status(self, bug_numbers):
        t = time()
        result = self.server.get_status(bug_numbers)
        print "BTS query time: ", time() - t

        # FIXME: looks like a bug in debbugs SOAP implementation
        # empty results turn out as "" or " "
        if result == "" or result == " ":
            return []

        if isinstance(result.item, list):
            ret = [item.value for item in result.item]
        else:
            ret = [result.item.value]

        # Fix statuses given by SOAP
        for item in ret:
            if item.pending == "pending":
                item.pending = "open"
            elif item.pending == "pending-fixed":
                item.pending = "pending"
            elif item.pending == "done":
                item.pending = "closed"

        return ret

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
        # this gives us only unique elements
        result = set(pkg + src)

        return list(result)

    def get_bug_log(self, bug):
        # FIXME: Not in BtsQueries
        result = self.server.get_bug_log(bug)
        return result

    def get_tagged_bugs(self, users):
        # FIXME: Not in BtsQueries
        # TODO: ask Don to allow many users at the same time
        result = []
        for user in users:
            result = result + self.server.get_usertag(user)
        return result
