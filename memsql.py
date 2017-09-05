from checks import AgentCheck
from contextlib import contextmanager

# 3rd party
from memsql.common import database

class MemSQL(AgentCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        host, port, user, password = self._get_config(instance)
        with self._connect(host, port, user, password) as db:
            try:
                db.execute('SELECT 1;')
            except Exception as e:
                self.log.exception("error!")
                raise e

    def _get_config(self, instance):
        self.host = instance.get('host', '')
        self.port = int(instance.get('port', 3306))
        user = instance.get('user', '')
        password = instance.get('password', '')

        return (self.host, self.port, user, password)

    @contextmanager
    def _connect(self, host, port, user, password):
        db = None
        try:
            db = database.connect(host=host, port=port, user=user, password=password)
            self.log.debug("Connected to MemSQL")
            yield db
        except Exception:
            raise
        finally:
            if db:
                db.close()
