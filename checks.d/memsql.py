from checks import AgentCheck

class MemSQL(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', 1)
