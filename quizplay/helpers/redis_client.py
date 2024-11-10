# In this version, we assume that Redis instances are dynamically set in config file config.yaml
# In product code, we should use a discovery service as Consul/K8s or setting up redis instances registering
# Zookeeper to dynamically manage them efficiently.

import redis
from hashring import HashRing
from redis import Redis


class RedisClient:
    def __init__(self):
        self.instances = {}
    def init_app(self, app):
        for idx, connection_str in enumerate(app.config['REDIS_NODES'].split(",")):
            host, port, db = connection_str.split(':')
            self.instances[idx] = redis.Redis(host=host, port=port, db=db)
    def get_instance(self, shard_key: str) -> Redis:
        ring = HashRing(self.instances.keys())
        return self.instances[ring.get_node(shard_key)]

class ClientBase:
    def __init__(self, client: RedisClient):
        self.redis = client