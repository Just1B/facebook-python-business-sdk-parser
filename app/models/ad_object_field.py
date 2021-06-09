from neo4j import GraphDatabase

from config import Config

from helpers.logger import LoggerMixin


class AdObjectField(LoggerMixin):
    def __init__(self):
        self._driver = GraphDatabase.driver(
            Config.NEO4J_HOST,
        )

    @classmethod
    def create_ad_object_field(cls, tx, ad_object_id, fields):
        return tx.run(
            "MATCH ( ao: AdObject ) WHERE ID(ao) = $ad_object_id "
            "UNWIND $fields as fields "
            "CREATE (ao)<-[:IS_FIELD]-(af:AdObjectField) SET af = fields",
            {"fields": fields, "ad_object_id": ad_object_id},
        )

    @classmethod
    def reset_the_world(clx, tx):
        return tx.run(" MATCH ( af:AdObjectField) DETACH DELETE af ")

    def add_ad_object_fields(self, ad_object_id, fields):
        with self._driver.session() as session:
            return session.write_transaction(
                self.create_ad_object_field, ad_object_id=ad_object_id, fields=fields
            )

    def reset_ad_object_fields(self):
        with self._driver.session() as session:
            return session.write_transaction(self.reset_the_world)
