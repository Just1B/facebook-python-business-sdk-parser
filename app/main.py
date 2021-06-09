# import time
import os
import ast
import json

from config import Config

from helpers.logger import get_app_logger

from models.ad_object import AdObject
from models.ad_object_field import AdObjectField
from models.ad_object_class import AdObjectClass
from models.ad_object_class_field import AdObjectClassField

logger = get_app_logger("FACEBOOK_SDK_PARSER")


def class_name_to_readable(className: str):

    output = ""
    for x in className:
        output += f"_{x.lower()}" if x.isupper() else x

    return output[1:]


def parse_tree(filename, tree):

    node = {
        "ad_object": {
            "sdk_filename": filename,
            "class_name": None,
            "readable_name": None,
        },
        "ad_object_fields": [],
        "ad_object_class": {},
    }

    for ctx in tree.body:

        # https://docs.python.org/3/library/ast.html#ast.ClassDef
        if isinstance(ctx, ast.ClassDef):

            node["ad_object"]["class_name"] = ctx.name
            node["ad_object"]["readable_name"] = class_name_to_readable(ctx.name)

            for ctx2 in ctx.body:

                # Fields for request params
                # Other class for params types

                # class XYZ():
                #     class Field(): -> contain all request params
                #
                #     _field_types {
                #       name : string,
                #       url : string,
                #       text : TextType
                #     }

                #     class TextType:
                #       custom = 'custom'
                #       disclaimer = 'disclaimer'
                #       from_price = 'from_price'

                # https://docs.python.org/3/library/ast.html#ast.Assign
                # https://docs.python.org/3/library/ast.html#ast.Name
                # https://docs.python.org/3/library/ast.html#ast.Dict
                if (
                    isinstance(ctx2, ast.Assign)
                    and ctx2.targets[0].id == "_field_types"
                ):

                    # ctx2.value -> ast.Dict()

                    keys = ctx2.value.keys
                    values = ctx2.value.values

                    for index, key in enumerate(keys):

                        node["ad_object_fields"].append(
                            {
                                "field": str(key.value),
                                "type": str(values[index].value),
                            }
                        )

                # We already parsed fields, just need other class
                if isinstance(ctx2, ast.ClassDef) and ctx2.name != "Field":

                    node["ad_object_class"][ctx2.name] = []

                    # list on ast.Assign
                    for x in ctx2.body:

                        node["ad_object_class"][ctx2.name].append(
                            {
                                "field": str(x.targets[0].id),
                                "type": str(x.value.value),
                            }
                        )

    return node


def main():

    FULL_FILES_LIST = os.listdir(Config.FULL_PATH)

    ADOBJECTS_FILES = list(filter((lambda x: ".py" in x), FULL_FILES_LIST))

    TO_PROCESS = [f for f in ADOBJECTS_FILES if f not in Config.EXCLUSION_LIST]

    logger.info(f"**** FOUND {len(TO_PROCESS)} files to parse ****\n")

    # RESET THE DATABASE
    AdObjectClassField().reset_ad_object_class_fields()
    AdObjectClass().reset_ad_object_class()
    AdObjectField().reset_ad_object_fields()
    AdObject().reset_ad_objects()

    for x in TO_PROCESS:

        with open(f"{Config.FULL_PATH}/{x}", "r") as source_file:
            tree = ast.parse(source_file.read())

        node = parse_tree(filename=x, tree=tree)

        # logger.info(node)

        try:
            logger.info(f" ++ TRYING TO INSERT : {node['ad_object']['class_name']}")

            id = AdObject().add_ad_object(node["ad_object"])

            AdObjectField().add_ad_object_fields(id, node["ad_object_fields"])

            for z in node["ad_object_class"]:

                ac_id = AdObjectClass().add_ad_object_class(id, {"class_name": z})

                AdObjectClassField().add_ad_object_class_fields(
                    ac_id, node["ad_object_class"][z]
                )

        except Exception as error:

            logger.error(f"Can't insert node : {error}")

    logger.info(f"**** PARSING DONE ****\n")


if __name__ == "__main__":
    main()