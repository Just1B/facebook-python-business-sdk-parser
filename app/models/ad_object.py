from neo4j import GraphDatabase

from config import Config

from helpers.logger import LoggerMixin


class AdObject(LoggerMixin):
    def __init__(self):
        self._driver = GraphDatabase.driver(
            Config.NEO4J_HOST,
        )

    @classmethod
    def create_ad_object(cls, tx, ad_object):
        result = tx.run(
            " CREATE ( ao:AdObject) SET ao = $ad_object RETURN id(ao)",
            ad_object=ad_object,
        )

        return result.single()[0]

    @classmethod
    def reset_the_world(clx, tx):
        return tx.run(" MATCH ( ao:AdObject) DETACH DELETE ao ")

    def add_ad_object(self, ad_object):
        with self._driver.session() as session:
            return session.write_transaction(self.create_ad_object, ad_object)

    def reset_ad_objects(self):
        with self._driver.session() as session:
            return session.write_transaction(self.reset_the_world)