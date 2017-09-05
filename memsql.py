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
                self._submit_leaves(db)
            except Exception as e:
                self.log.error("fail to send metrics to datadog")

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

    def _submit_leaves(self, db):
        try:
            res = db.query('SHOW LEAVES;')
            if res is not None:
                self.count('memsql.leaves.count', len(res), tags=['leaves'])
                sum_latency = 0
                for i in res:
                    sum_latency += i['Average_Roundtrip_Latency_ms']

                self.gauge('memsql.leaves.avg_roundtrip_latency', sum_latency/len(res), tags=['leaves'])

        except Exception as e:
            self.log.error("fail to execute _get_leaves")
            return None