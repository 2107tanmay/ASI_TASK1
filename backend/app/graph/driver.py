class DummySession:
    def close(self): pass
    def run(self, *args, **kwargs): pass

class Neo4jDriver:
    def close(self): pass
    def session(self, **kwargs): return DummySession()

neo4j_driver = Neo4jDriver()
