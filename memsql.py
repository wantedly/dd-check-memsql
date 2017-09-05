from checks import AgentCheck

class MemSQL(AgentCheck):
    def check(self, instance):
        host, port, user, password = self._get_config(instance)
        self.gauge('hello.world', 1)

    def _get_config(self, instance):
        self.host = instance.get('host', '')
        self.port = int(instance.get('port', 3306))
        user = instance.get('user', '')
        password = instance.get('password', '')

        return (self.host, self.port, user, password)