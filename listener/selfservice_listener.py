from univention.listener.handler import ListenerModuleHandler


class SelfserviceListener(ListenerModuleHandler):
    """
    Listener module that creates a file on a folder if the newly created user
    has the attribute `univentionPasswordSelfServiceEmail` set.
    """

    def initialize(self):
        self.logger.info("[ initialize ] SelfserviceListener")

    def create(self, dn, new):
        self.logger.info("[ create ] dn: %r", dn)
        self.logger.debug(new)

    class Configuration(ListenerModuleHandler.Configuration):
        name = "selfservice-listener"
        description = "Self Service user invite listener"
        ldap_filter = "(objectClass=users/user)"
