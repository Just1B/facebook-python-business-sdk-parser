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
        return tx.run(" CREATE ( u:AdObject) SET u = $ad_object ", ad_object=ad_object)

    @classmethod
    def reset_the_world(clx, tx):
        return tx.run(" MATCH ( u:AdObject) DELETE u ")

    def add_ad_object(self, ad_object):
        with self._driver.session() as session:
            return session.write_transaction(self.create_ad_object, ad_object)

    def reset_ad_object(self):
        with self._driver.session() as session:
            return session.write_transaction(self.reset_the_world)