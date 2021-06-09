from neo4j import GraphDatabase

from config import Config

from helpers.logger import LoggerMixin


class AdObjectClass(LoggerMixin):
    def __init__(self):
        self._driver = GraphDatabase.driver(
            Config.NEO4J_HOST,
        )

    @classmethod
    def create_ad_object_class(cls, tx, ad_object_id, ad_object_class):
        result = tx.run(
            "MATCH ( ao: AdObject ) WHERE ID(ao) = $ad_object_id "
            "CREATE (ao)<-[:IS_CLASS]-(ac:AdObjectClass) SET ac = $ad_object_class "
            "RETURN id(ac)",
            {"ad_object_class": ad_object_class, "ad_object_id": ad_object_id},
        )

        return result.single()[0]

    @classmethod
    def reset_the_world(clx, tx):
        return tx.run(" MATCH ( ac:AdObjectClass) DETACH DELETE ac ")

    def add_ad_object_class(self, ad_object_id, ad_object_class):
        with self._driver.session() as session:
            return session.write_transaction(
                self.create_ad_object_class,
                ad_object_id=ad_object_id,
                ad_object_class=ad_object_class,
            )

    def reset_ad_object_class(self):
        with self._driver.session() as session:
            return session.write_transaction(self.reset_the_world)
