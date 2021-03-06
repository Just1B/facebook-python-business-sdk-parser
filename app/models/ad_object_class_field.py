from neo4j import GraphDatabase

from config import Config

from helpers.logger import LoggerMixin


class AdObjectClassField(LoggerMixin):
    def __init__(self):
        self._driver = GraphDatabase.driver(
            Config.NEO4J_HOST,
        )

    @classmethod
    def create_ad_object_class_fields(cls, tx, ad_object_class_id, class_fields):
        return tx.run(
            "MATCH ( ac: AdObjectClass ) WHERE ID(ac) = $ad_object_class_id "
            "UNWIND $class_fields as class_fields "
            "CREATE (ac)<-[:IS_CLASS_FIELD]-(acf:AdObjectClassField) SET acf = class_fields",
            {"class_fields": class_fields, "ad_object_class_id": ad_object_class_id},
        )

    @classmethod
    def reset_the_world(clx, tx):
        return tx.run(" MATCH ( ac:AdObjectClassField) DETACH DELETE ac ")

    def add_ad_object_class_fields(self, ad_object_class_id, class_fields):
        with self._driver.session() as session:
            return session.write_transaction(
                self.create_ad_object_class_fields,
                ad_object_class_id=ad_object_class_id,
                class_fields=class_fields,
            )

    def reset_ad_object_class_fields(self):
        with self._driver.session() as session:
            return session.write_transaction(self.reset_the_world)
